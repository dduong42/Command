class command(object):
    def __init__(self, function):
        self.function = function
        self.inverse = None

    def __rshift__(self, other):
        def func(context):
            return other(self(context))
        def inv(context):
            return self.inverse(other.inverse(context))

        new_command = command(function=func)
        inv = inverse_of(new_command)(inv)
        return new_command

    def __call__(self, context):
        return self.function(context)


def inverse_of(cmd):
    def decorator(inverse):
        inv_cmd = command(inverse)
        inv_cmd.inverse = cmd

        cmd.inverse = inv_cmd
        return inv_cmd
    return decorator
