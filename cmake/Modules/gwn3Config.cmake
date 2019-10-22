INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_GWN3 gwn3)

FIND_PATH(
    GWN3_INCLUDE_DIRS
    NAMES gwn3/api.h
    HINTS $ENV{GWN3_DIR}/include
        ${PC_GWN3_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GWN3_LIBRARIES
    NAMES gnuradio-gwn3
    HINTS $ENV{GWN3_DIR}/lib
        ${PC_GWN3_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gwn3Target.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GWN3 DEFAULT_MSG GWN3_LIBRARIES GWN3_INCLUDE_DIRS)
MARK_AS_ADVANCED(GWN3_LIBRARIES GWN3_INCLUDE_DIRS)
