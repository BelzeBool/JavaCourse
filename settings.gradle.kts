rootProject.name = "java-mods-course"

pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

plugins {
    // Позволяет Gradle самому скачать нужную версию JDK, если её нет на компьютере
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

// Каждая папка задачи (где есть src/) становится отдельным модулем
rootProject.projectDir.walkTopDown()
    .onEnter { dir -> dir.name !in setOf(".git", ".idea", ".gradle", "build", "common", "gradle") }
    .filter { it.isDirectory && File(it, "src").isDirectory }
    .forEach { taskDir ->
        val relative = rootDir.toPath().relativize(taskDir.toPath())
        val moduleName = relative.joinToString("-") { it.toString().replace(Regex("[^A-Za-z0-9_]"), "_") }
        include(moduleName)
        project(":$moduleName").projectDir = taskDir
    }

include("common")
