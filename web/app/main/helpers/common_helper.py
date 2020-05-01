

class UtilHelper(object):

    @staticmethod
    def show_module_path(module):
        import imp, sys, inspect
        if (hasattr(module, '__name__') is False):
            print('Error: ' + str(module) + ' is not a module object.')
            return None
        moduleName = module.__name__
        modulePath = None
        if imp.is_builtin(moduleName):
            modulePath = sys.modules[moduleName];
        else:
            modulePath = inspect.getsourcefile(module)
            modulePath = '<module \'' + moduleName + '\' from \'' + modulePath + 'c\'>'
        print(modulePath)
        return modulePath
