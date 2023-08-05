
#ifndef DLLEXPORT_H
#define DLLEXPORT_H

#ifdef SHARED_EXPORTS_BUILT_AS_STATIC
#  define DLLEXPORT
#  define SWMM_OUTPUT_NO_EXPORT
#else
#  ifndef DLLEXPORT
#    ifdef swmm_output_EXPORTS
        /* We are building this library */
#      define DLLEXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define DLLEXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef SWMM_OUTPUT_NO_EXPORT
#    define SWMM_OUTPUT_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef SWMM_OUTPUT_DEPRECATED
#  define SWMM_OUTPUT_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef SWMM_OUTPUT_DEPRECATED_EXPORT
#  define SWMM_OUTPUT_DEPRECATED_EXPORT DLLEXPORT SWMM_OUTPUT_DEPRECATED
#endif

#ifndef SWMM_OUTPUT_DEPRECATED_NO_EXPORT
#  define SWMM_OUTPUT_DEPRECATED_NO_EXPORT SWMM_OUTPUT_NO_EXPORT SWMM_OUTPUT_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef SWMM_OUTPUT_NO_DEPRECATED
#    define SWMM_OUTPUT_NO_DEPRECATED
#  endif
#endif

#endif /* DLLEXPORT_H */
