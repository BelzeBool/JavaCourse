import java.io.ByteArrayOutputStream

// Сборка курса «Java с нуля: от первой строчки до своего мода»
// Каждая папка задачи (где есть src/) — отдельный Gradle-модуль, см. settings.gradle.kts.

fun gradleProperties(key: String) = providers.gradleProperty(key)

group = gradleProperties("courseGroup").get()
version = gradleProperties("courseVersion").get()

plugins {
    java
}

allprojects {
    repositories {
        mavenCentral()
    }
}

configure(subprojects) {
    apply(plugin = "java")

    dependencies {
        val junitVersion = "5.11.4"
        "testImplementation"("org.junit.jupiter:junit-jupiter-api:$junitVersion")
        "testRuntimeOnly"("org.junit.jupiter:junit-jupiter-engine:$junitVersion")
        "testRuntimeOnly"("org.junit.platform:junit-platform-launcher:1.11.4")
    }

    val jvmVersion = gradleProperties("jvmVersion").get().toInt()
    extensions.configure<JavaPluginExtension> {
        toolchain.languageVersion.set(JavaLanguageVersion.of(jvmVersion))
    }

    tasks.withType<JavaCompile> {
        options.encoding = "UTF-8"
    }

    // Эта часть нужна плагину JetBrains Academy: он читает строки #educational_plugin
    // и показывает текст ошибки в панели задачи.
    tasks.withType<Test> {
        useJUnitPlatform()
        systemProperty("file.encoding", "UTF-8")
        systemProperty("stdout.encoding", "UTF-8")
        outputs.upToDateWhen { false }

        addTestListener(object : TestListener {
            override fun beforeSuite(suite: TestDescriptor) {}
            override fun beforeTest(testDescriptor: TestDescriptor) {}
            override fun afterTest(testDescriptor: TestDescriptor, result: TestResult) {
                if (result.resultType == TestResult.ResultType.FAILURE) {
                    val message = result.exception?.message ?: "Неверный ответ"
                    val lines = message.split("\n")
                    println("#educational_plugin FAILED + ${lines[0]}")
                    lines.subList(1, lines.size).forEach { line ->
                        println("#educational_plugin$line")
                    }
                    println()
                }
            }
            override fun afterSuite(suite: TestDescriptor, result: TestResult) {}
        })
    }
}

// В задачах код лежит прямо в src/, тесты — в test/
configure(subprojects.filter { it.name != "common" }) {
    extensions.configure<SourceSetContainer> {
        getByName("main").java.srcDirs("src")
        getByName("test").java.srcDirs("test")
    }

    dependencies {
        "testImplementation"(project(":common"))
    }

    // Задача run: её вызывает плагин для задач типа output (проверка по выводу без тестов).
    // Плагин передаёт -PmainClass=... и -PeducationalRun=true и читает вывод по строкам #educational_plugin.
    apply(plugin = "application")
    extensions.configure<JavaApplication> {
        mainClass.set(providers.gradleProperty("mainClass").orElse("Main"))
    }
    tasks.named<JavaExec>("run") {
        jvmArgs("-Dfile.encoding=UTF-8", "-Dstdout.encoding=UTF-8")
        standardInput = System.`in`
        if (providers.gradleProperty("educationalRun").orNull == "true") {
            val runOutput = ByteArrayOutputStream()
            standardOutput = runOutput
            doLast {
                println("#educational_plugin_checker_version 1")
                val separator = System.lineSeparator()
                runOutput.toString(Charsets.UTF_8)
                    .split(Regex("(?<=$separator)|(?=$separator)"))
                    .forEach { println("#educational_plugin$it") }
            }
        }
    }
}
