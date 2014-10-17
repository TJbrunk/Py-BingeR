def main():
    from distutils.core import setup
    import py2exe


    setup(console=['Main.py'],

            options = {
                'includes':'accounts.csv'
                }
         )

if __name__ == '__main__':
    main()
