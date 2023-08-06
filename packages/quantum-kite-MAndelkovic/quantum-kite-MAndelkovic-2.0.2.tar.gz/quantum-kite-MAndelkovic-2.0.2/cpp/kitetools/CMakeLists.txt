cmake_minimum_required(VERSION 3.9)
project(KITE-tools CXX)

set(CMAKE_CXX_STANDARD 17)
set(KITE_TOOLS_WARNING_FLAGS -Wall -Wextra -Wpedantic)

set(SYSTEM_NAME "${CMAKE_HOST_SYSTEM_NAME}")
cmake_host_system_information(RESULT _host_name QUERY HOSTNAME)
set(MACHINE_NAME "${_host_name}")
string(TIMESTAMP TODAY "(yymmdd) %Y-%m-%d %H:%M:%S")
add_definitions(-DTIMESTAMP=${TIMESTAMP} -DMACHINE_NAME="${MACHINE_NAME}" -DSYSTEM_NAME="${SYSTEM_NAME}")

add_library(kitetoolscpp
        include/cond_2order/conductivity_2order.hpp
        include/cond_2order/Gamma0.hpp
        include/cond_2order/Gamma0photo.hpp
        include/cond_2order/Gamma1.hpp
        include/cond_2order/Gamma1photo.hpp
        include/cond_2order/Gamma2.hpp
        include/cond_2order/Gamma2photo.hpp
        include/cond_2order/Gamma3.hpp
        include/cond_2order/Gamma3photo.hpp
        include/cond_dc/conductivity_dc.hpp
        include/arpes.hpp
        include/calculate.hpp
        include/ComplexTraits.hpp
        include/conductivity_optical.hpp
        include/compiletime_info.hpp
        include/dos.hpp
        include/functions.hpp
        include/ldos.hpp
        include/macros.hpp
        include/messages.hpp
        include/myHDF5.hpp
        include/parse_input.hpp
        include/systemInfo.hpp

        src/cond_2order/conductivity_2order.cpp
        src/cond_2order/Gamma0.cpp
        src/cond_2order/Gamma0photo.cpp
        src/cond_2order/Gamma1.cpp
        src/cond_2order/Gamma1photo.cpp
        src/cond_2order/Gamma2.cpp
        src/cond_2order/Gamma2photo.cpp
        src/cond_2order/Gamma3.cpp
        src/cond_2order/Gamma3photo.cpp
        src/cond_dc/conductivity_dc.cpp
        src/cond_dc/fill.cpp
        src/arpes.cpp
        src/calculate.cpp
        src/compiletime_info.h.in
        src/conductivity_optical.cpp
        src/dos.cpp
        src/functions.cpp
        src/ldos.cpp
        src/myHDF5.cpp
        src/parse_input.cpp
        src/systemInfo.cpp
        )

target_include_directories(kitetoolscpp PUBLIC include)

find_package(HDF5 COMPONENTS CXX C HL)
if (${HDF5_FOUND})
    set(HDF5_USE_STATIC_LIBRARIES ON)
    target_include_directories(kitetoolscpp PUBLIC ${HDF5_INCLUDE_DIR})
    target_link_libraries(kitetoolscpp PUBLIC ${HDF5_CXX_LIBRARIES})

    MESSAGE(STATUS "Hdf5 Library: ${HDF5_CXX_HL_LIBRARIES}")
    MESSAGE(STATUS "Hdf5Hl Library: ${HDF5_CXX_LIBRARIES}")
    MESSAGE(STATUS "Compiler: ${CMAKE_CXX_COMPILER}")
else ()
    MESSAGE(FATAL_ERROR "Couldn't find hdf5")
endif ()

find_package(Eigen3)
if (${EIGEN3_FOUND})
    target_include_directories(kitetoolscpp PUBLIC ${EIGEN3_INCLUDE_DIR})
    MESSAGE(STATUS "Eigen Library: ${EIGEN3_INCLUDE_DIR}")
else ()
    MESSAGE(STATUS "Couldn't find Eigen3. Looking in ~/include/eigen3")
    target_include_directories(kitetoolscpp PUBLIC ~/include/eigen3)
endif ()

find_package(OpenMP)
MESSAGE(STATUS "OPENMP: ${OPENMP_FOUND}")
if (OpenMP_CXX_FOUND)
    target_link_libraries(kitetoolscpp PUBLIC OpenMP::OpenMP_CXX)
    set(KITE_TOOLS_COMPILATION_FLAGS ${OpenMP_CXX_FLAGS})
    MESSAGE(STATUS "OpenMP Library: ${EIGEN3_INCLUDE_DIR}")
else ()
    MESSAGE(STATUS "Couldn't find OpenMP.")
endif ()

set(RELEASE_FLAGS ${KITE_TOOLS_COMPILATION_FLAGS} ${KITE_TOOLS_WARNING_FLAGS} -O3)
set(DEBUG_FLAGS ${KITE_TOOLS_COMPILATION_FLAGS} ${KITE_TOOLS_WARNING_FLAGS} -g)
if (CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(kitetoolscpp PRIVATE $<$<CONFIG:DEBUG>:${DEBUG_FLAGS}>)
    target_compile_options(kitetoolscpp PRIVATE $<$<CONFIG:RELEASE>:${RELEASE_FLAGS}>)
    target_compile_options(kitetoolscpp PUBLIC -fvisibility=hidden)

endif ()
