add_executable(lrcalc-bin lrcalc.c)
# target_compile_features(lrcalc-bin PRIVATE cxx_std_17)
target_link_libraries(lrcalc-bin PRIVATE lrcalc)

# Cross-platform compiler lints
if (${CMAKE_C_COMPILER_ID} STREQUAL "Clang"
        OR ${CMAKE_C_COMPILER_ID} STREQUAL "GNU")
    target_compile_options(lrcalc-bin PRIVATE
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
    target_compile_options(lrcalc-bin PRIVATE
            /W3)
endif ()

set_target_properties(lrcalc-bin PROPERTIES OUTPUT_NAME lrcalc)

add_custom_command(
        TARGET lrcalc-bin
        PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -DSRC_DIR="${CMAKE_SOURCE_DIR}/data" -DDEST_DIR="${CMAKE_CURRENT_BINARY_DIR}/data" -P "${CMAKE_SOURCE_DIR}/cmake/configure_files.cmake"
)


# Same for apps/schubmult.c.
add_executable(schubmult-bin schubmult.c)
# target_compile_features(schubmult-bin PRIVATE cxx_std_17)
target_link_libraries(schubmult-bin PRIVATE lrcalc)

# Cross-platform compiler lints
if (${CMAKE_C_COMPILER_ID} STREQUAL "Clang"
        OR ${CMAKE_C_COMPILER_ID} STREQUAL "GNU")
    target_compile_options(schubmult-bin PRIVATE
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
    target_compile_options(schubmult-bin PRIVATE
            /W3)
endif ()

set_target_properties(schubmult-bin PROPERTIES OUTPUT_NAME schubmult)

add_custom_command(
        TARGET schubmult-bin
        PRE_BUILD
        COMMAND ${CMAKE_COMMAND} -DSRC_DIR="${CMAKE_SOURCE_DIR}/data" -DDEST_DIR="${CMAKE_CURRENT_BINARY_DIR}/data" -P "${CMAKE_SOURCE_DIR}/cmake/configure_files.cmake"
)
