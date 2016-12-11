#!/usr/bin/env python
import sys, os
sys.path.append(os.path.dirname(__file__))

if __name__ == '__main__':
    from c_ext.main import main
    main()
