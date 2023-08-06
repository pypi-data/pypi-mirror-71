# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.14.3)

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(discreture-populate NONE)

include(ExternalProject)
ExternalProject_Add(discreture-populate
                     "UPDATE_DISCONNECTED" "False" "GIT_REPOSITORY" "https://github.com/mraggi/discreture.git" "GIT_TAG" "v1.1"
                    SOURCE_DIR          "/home/david/playground/summer-2020/research/nlnum/cmake-build-release/_deps/discreture-src"
                    BINARY_DIR          "/home/david/playground/summer-2020/research/nlnum/cmake-build-release/_deps/discreture-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
)
