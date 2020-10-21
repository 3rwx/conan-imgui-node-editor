from conans import ConanFile, CMake, tools
import shutil
import os


CMAKELISTS = r"""
cmake_minimum_required(VERSION 3.12)

project(imgui-node-editor)

# Define IMGUI_NODE_EDITOR_ROOT_DIR pointing to project root directory
get_filename_component(IMGUI_NODE_EDITOR_ROOT_DIR ${CMAKE_SOURCE_DIR} ABSOLUTE CACHE)

# Point CMake where to look for module files.
list(APPEND CMAKE_MODULE_PATH ${IMGUI_NODE_EDITOR_ROOT_DIR}/misc/cmake-modules)

# Node editor use C++14
set(CMAKE_CXX_STANDARD            14)
set(CMAKE_CXX_STANDARD_REQUIRED   YES)

find_package(imgui REQUIRED)
include_directories(${imgui_INCLUDE_DIRS})
find_package(imgui_node_editor REQUIRED)

"""

class ImGuiNodeEditorConan(ConanFile):
    name = "imgui-node-editor"
    license = "MIT"
    url = "https://github.com/3rwx/conan-imgui-node-editor"
    description = "An implementation of node editor with ImGui-like API"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "cmake_find_package"

    def requirements(self):
        self.requires("imgui/1.78")

    def set_version(self):
        git = tools.Git(folder=self.recipe_folder)
        self.version = "%s_%s" % (git.get_branch(), git.get_revision())

    def source(self):
        self.run("git clone https://github.com/thedmd/imgui-node-editor.git")
        shutil.rmtree("imgui-node-editor/external/imgui")
        os.remove("imgui-node-editor/misc/cmake-modules/Findimgui.cmake")
        with open("imgui-node-editor/CMakeLists.txt", "wb") as f:
            f.write(CMAKELISTS.encode("ascii"))

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="imgui-node-editor")
        cmake.build()

    def package(self):
        self.copy("imgui_node_editor.h", dst="include", src="imgui-node-editor")
        self.copy("*.lib", dst="lib", keep_path=False, excludes="*/external/*")
        self.copy("*.a", dst="lib", keep_path=False, excludes="*/external/*")

    def package_info(self):
        self.cpp_info.libs = ["imgui_node_editor"]
