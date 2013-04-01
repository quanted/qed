#include <string.h>

    void   copyi_ ( arLen, arIn, arOut)

    int         *arLen;
    char        *arIn, *arOut;

    {
        int  Len;
        Len = (*arLen)*4;
        (void) memcpy (arOut, arIn, Len);
    }

    void   copyr_ ( arLen, arIn, arOut)

    int         *arLen;
    char        *arIn, *arOut;

    {
        int  Len;

        Len = (*arLen)*4;
        (void) memcpy (arOut, arIn, Len);
    }

    void   copyd_ ( arLen, arIn, arOut)

    int         *arLen;
    char        *arIn, *arOut;

    {
        int  Len;

        Len = (*arLen)*8;
        (void) memcpy (arOut, arIn, Len);
    }

    void   copyc_ ( arLen, arIn, arOut)

    int         *arLen;
    char        *arIn, *arOut;

    {
        int  Len;

        Len = *arLen;
        (void) memcpy (arOut, arIn, Len);
    }

    void   zipi_ ( arLen, arIn, arOut)

    int         *arLen;
    int         *arIn, *arOut;

    {
        int  Len;
        Len = *arLen;
        while ( Len-- > 0 )
          *arOut++ = *arIn ;
    }

    void   zipr_ ( arLen, arIn, arOut)

    int         *arLen;
    float       *arIn, *arOut;

    {
        int  Len;
        Len = *arLen;
        while ( Len-- > 0 )
          *arOut++ = *arIn ;
    }

    void   zipd_ ( arLen, arIn, arOut)

    int         *arLen;
    double      *arIn, *arOut;

    {
        int  Len;
        Len = *arLen;
        while ( Len-- > 0 )
          *arOut++ = *arIn ;
    }

    void   zipc_ ( arLen, arIn, arOut)

    int         *arLen;
    char        *arIn, *arOut;

    {
        int  Len;

        Len = *arLen;
        (void) memset ( arOut, *arIn, Len );
    }
