def main():
    from distutils.core import setup
    import py2exe


    setup(console=['Py-BingeR.py'],
         )

if __name__ == '__main__':
    main()
    #call this file from the command line as follows
    #python setup.py py2exe
