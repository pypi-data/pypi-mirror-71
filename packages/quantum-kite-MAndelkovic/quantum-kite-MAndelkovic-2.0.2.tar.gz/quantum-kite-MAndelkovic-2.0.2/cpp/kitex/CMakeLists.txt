cmake_minimum_required(VERSION 3.9)
project(KITEx)

set(CMAKE_CXX_STANDARD 17)
set(KITEx_WARNING_FLAGS -Wall -Wextra -Wpedantic)

add_library(kitecpp
        include/ComplexTraits.hpp
        include/Coordinates.hpp
        include/Generic.hpp
        include/Global.hpp
        include/Hamiltonian.hpp
        include/HamiltonianDefects.hpp
        include/HamiltonianRegular.hpp
        include/HamiltonianVacancies.hpp
        include/KPM_Vector.hpp
        include/KPM_Vector2D.hpp
        include/KPM_Vector3D.hpp
        include/KPM_VectorBasis.hpp
        include/LatticeStructure.hpp
        include/messages.hpp
        include/myHDF5.hpp
        include/queue.hpp
        include/Random.hpp
        include/Simulation.hpp
        include/SimulationGlobal.hpp

        src/ComplexTraits.cpp
        src/Coordinates.cpp
        src/Gamma1D.cpp
        src/Gamma2D.cpp
        src/Gamma3D.cpp
        src/Global.cpp
        src/GlobalSimulation.cpp
        src/Hamiltonian.cpp
        src/HamiltonianDefects.cpp
        src/HamiltonianRegular.cpp
        src/HamiltonianVacancies.cpp
        src/KPM_Vector.cpp
        src/KPM_Vector2D.cpp
        src/KPM_Vector3D.cpp
        src/KPM_VectorBasis.cpp
        src/LatticeStructure.cpp
        src/myHDF5.cpp
        src/queue.cpp
        src/Random.cpp
        src/recursive_kpm.cpp
        src/Simulation.cpp
        src/SimulationARPES.cpp
        src/SimulationCondDC.cpp
        src/SimulationCondOpt.cpp
        src/SimulationCondOpt2.cpp
        src/SimulationDOS.cpp
        src/SimulationGaussianWavePacket.cpp
        src/SimulationLMU.cpp
        src/SimulationSingleShot.cpp
        )

target_include_directories(kitecpp PUBLIC include)

find_package(HDF5 COMPONENTS CXX C HL)
if (${HDF5_FOUND})
    set(HDF5_USE_STATIC_LIBRARIES ON)
    target_include_directories(kitecpp PUBLIC ${HDF5_INCLUDE_DIR})
    target_link_libraries(kitecpp PUBLIC ${HDF5_CXX_LIBRARIES})

    MESSAGE(STATUS "Hdf5 Library: ${HDF5_CXX_HL_LIBRARIES}")
    MESSAGE(STATUS "Hdf5Hl Library: ${HDF5_CXX_LIBRARIES}")
    MESSAGE(STATUS "Compiler: ${CMAKE_CXX_COMPILER}")
else ()
    MESSAGE(FATAL_ERROR "Couldn't find hdf5")
endif ()

find_package(Eigen3)
if (${EIGEN3_FOUND})
    target_include_directories(kitecpp PUBLIC ${EIGEN3_INCLUDE_DIR})
    MESSAGE(STATUS "Eigen Library: ${EIGEN3_INCLUDE_DIR}")
else ()
    MESSAGE(STATUS "Couldn't find Eigen3. Looking in ~/include/eigen3")
    target_include_directories(kitecpp PUBLIC ~/include/eigen3)
endif ()

find_package(OpenMP)
MESSAGE(STATUS "OPENMP: ${OPENMP_FOUND}")
if (OpenMP_CXX_FOUND)
    target_link_libraries(kitecpp PUBLIC OpenMP::OpenMP_CXX)
    set(KITE_TOOLS_COMPILATION_FLAGS ${OpenMP_CXX_FLAGS})
    MESSAGE(STATUS "OpenMP Library: ${EIGEN3_INCLUDE_DIR}")
else ()
    MESSAGE(STATUS "Couldn't find OpenMP.")
endif ()

set(RELEASE_FLAGS ${KITE_TOOLS_COMPILATION_FLAGS} ${KITE_TOOLS_WARNING_FLAGS} -O3)
set(DEBUG_FLAGS ${KITE_TOOLS_COMPILATION_FLAGS} ${KITE_TOOLS_WARNING_FLAGS} -g)
if (CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(kitecpp PRIVATE $<$<CONFIG:DEBUG>:${DEBUG_FLAGS}>)
    target_compile_options(kitecpp PRIVATE $<$<CONFIG:RELEASE>:${RELEASE_FLAGS}>)
    target_compile_options(kitecpp PUBLIC -fvisibility=hidden)

    if (CMAKE_CXX_COMPILER_ID MATCHES "GNU")
        set(compile_wp 1)
        if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 7.1.0)
            MESSAGE(STATUS "Cannot compile gaussian wavepacket! Bessel functions are available from C++17 GCC 7.1.0")
            set(compile_wp 0)
        endif ()
    endif()

    if (CMAKE_CXX_COMPILER_ID MATCHES "CLANG")
        set(compile_wp 1)
        if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 5.0.0)
            MESSAGE(STATUS "Cannot compile gaussian wavepacket! Bessel functions are available from C++17 CLANG 5.0.0")
            set(compile_wp 0)
        endif ()
    endif()

    target_compile_options(kitecpp PRIVATE -DCOMPILE_WAVEPACKET=${compile_wp})
endif ()
