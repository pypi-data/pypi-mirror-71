file(GLOB SOURCE_LIST CONFIGURE_DEPENDS
        "${LRCalc_SOURCE_DIR}/tests/*.h"
        "${LRCalc_SOURCE_DIR}/tests/*.c")

# This target runs all of the tests.
# Make sure CATCH_CONFIG_MAIN is only defined in one test file.
add_executable(test-lrcalc ${SOURCE_LIST})

# We're using C++17 in the test
# target_compile_features(test-lrcalc PRIVATE cxx_std_17)

# Should be linked to the main library, as well as the Catch2 testing library
target_link_libraries(test-lrcalc PRIVATE lrcalc)

# If you register a test, then ctest and make test will run it.
# You can also run examples and check the output, as well.
add_test(NAME test-lrcalc COMMAND test-lrcalc) # Command can be a target

# Add folders
set_target_properties(test-lrcalc PROPERTIES FOLDER iclue)

# Cross-platform compiler lints
if (${CMAKE_C_COMPILER_ID} STREQUAL "Clang"
        OR ${CMAKE_C_COMPILER_ID} STREQUAL "GNU")
    target_compile_options(test-lrcalc PRIVATE
            -Wall
            -Wextra
            -Wswitch
            -Wconversion
            -Wparentheses
            -Wfloat-equal
            -Wzero-as-null-pointer-constant
            -Wpedantic
            -pedantic
            -pedantic-errors)
elseif (${CMAKE_C_COMPILER_ID} STREQUAL "MSVC")
    target_compile_options(test-lrcalc PRIVATE
            /W3)
endif ()


add_custom_command(
        TARGET test-lrcalc
        PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -DSRC_DIR="${CMAKE_CURRENT_SOURCE_DIR}/data" -DDEST_DIR="${CMAKE_CURRENT_BINARY_DIR}/data" -P "${CMAKE_SOURCE_DIR}/cmake/configure_files.cmake"
)

