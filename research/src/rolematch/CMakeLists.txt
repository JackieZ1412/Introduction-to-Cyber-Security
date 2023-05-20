cmake_minimum_required(VERSION 3.10)

project(Rolematch)

set(CMAKE_CXX_STANDARD 11)

include_directories(include)

file(GLOB SOURCES "src/*.cpp")

add_executable(Rolematch ${SOURCES})

target_link_libraries(Rolematch pthread)