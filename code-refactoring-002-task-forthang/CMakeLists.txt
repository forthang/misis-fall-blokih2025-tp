cmake_minimum_required(VERSION 3.16)
project(RefactoringForTestability)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add subdirectories
add_subdirectory(020-hardcoded_dependencies)
add_subdirectory(050-time)  
add_subdirectory(080-singletons)
add_subdirectory(test)
