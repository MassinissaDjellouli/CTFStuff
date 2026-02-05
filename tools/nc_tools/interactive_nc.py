import readline

from pwnlib import *
from pwnlib.tubes.tube import tube as Tube
class InteractiveNC:
    """
    Class to interact with a remote connection or process in an interactive way.
    It allows to store variables, perform operations on them and evaluate expressions.
    
    Contains 2 modes: interactive and non-interactive.
    
    Interactive mode allows to perform operations on the variables and evaluate expressions.\\
    Non-interactive mode allows to send inputs to the remote connection or process.
    
    To enter interactive mode, type the command prefix followed by "i" and press enter.\\
    To exit interactive mode, type the command prefix followed by "b" and press enter.
    
    Run the help command in interactive mode to see the available commands and their description.\\
    The command prefix is customizable and is set to "#$" by default.
    
    
    :param tube: The tube to interact with
    :param vars: A dictionary of initial variables
    :param command_prefix: The prefix to use for commands

    Example:
    ```python
    import pwnlib.tubes.process as process
    from interactive_nc import InteractiveNC
    r = process.process(["/test"])
    interactive = InteractiveNC(r,command_prefix="!")
    interactive.add_input("!v fmtstr %6$s")
    interactive.add_input("!b")
    interactive.add_input("0")
    interactive.add_input("!fmtstr")
    interactive.interactive()
    # Prints the first arg on the stack
    # Gives you back the control after the inputs are executed
    ```
    """

    def __init__(self, tube:Tube, vars: dict[str, bytes]|None=None, command_prefix="#$"):
        if vars is None:
            vars = {}
        self.r: Tube = tube
        self.vars: dict[str, bytes] = dict(
            [(k, v if isinstance(v, bytes) else v.encode()) for k, v in vars.items()]
        )
        self.back_from_interactive = False
        self.last_received: bytes = b""
        self.command_prefix = command_prefix
        self._commands = {}
        self.add_command("b", self._back_command)
        self.add_command("s", self._store_command)
        self.add_command("+", self._add_command)
        self.add_command("-", self._sub_command)
        self.add_command("*", self._mul_command)
        self.add_command("/", self._div_command)
        self.add_command("a", self._append_command)
        self.add_command("sl", self._slice_command)
        self.add_command("v", self._add_var_command)
        self.add_command("d", self._dump_vars_command)
        self.add_command("p", self._print_last_received_command)
        self.add_command("16", self._hex_command)
        self.add_command("10", self._dec_command)
        self.add_command("e", self._eval_command)
        self.add_command("h", self._help_command)
        self.add_command("c", self._copy_command)
        self.add_command("q", self._quit_command)
        self.add_command("pid", self._pid_command)
        self._input_queue = []

    def set_vars(self, vars: dict[str, bytes]):
        self.vars = vars

    def add_command(self, name: str, func):
        """
        Add a command to the interactive session

        The function __name__ needs to start with an underscore followed by the command name. (ex: _test_command)\\
        The function needs to take a list of strings as argument and needs to return a boolean.\\
        True to stay in interactive mode and False to go back to the main loop

        If docstring is present, it will be displayed when running the help command
        
        :param name: The name of the command
        :param func: The function to execute when the command is called
        """
        if not func.__name__.startswith("_"):
            print(
                f"Warning: command {name} is named {func.__name__}, which does not start with an underscore. Command ignored."
            )
            return
        if name in self._commands:
            print(f"Warning: command {name} already exists. Command ignored.")
            return
        argc = func.__code__.co_argcount
        if 1 > argc > 2:
            print(
                f"Warning: command {name} has {argc} arguments. Expected 1. Command ignored."
            )
            return

        if argc == 2 and func.__code__.co_varnames[0] != "self":
            print(
                f"Warning: command {name} has an invalid first argument. Expected self. Command ignored."
            )
            return

        if (
            func.__code__.co_varnames[argc - 1] not in func.__annotations__
            or func.__annotations__[func.__code__.co_varnames[argc - 1]] != list[str]
        ):
            print(
                f"Warning: command {name} has an invalid argument type. Expected list[str]. Command ignored."
            )
            return

        if func.__annotations__.get("return", None) != bool:
            print(
                f"Warning: command {name} has an invalid return type. Expected bool. Command ignored."
            )
            return

        self._commands[name] = func

    def _command_prefix(self) -> str:
        return self.command_prefix

    def add_input(self, inp: str):
        """
        Add an input to the input queue to be run in the interactive session

        :param inp: The input to add
        """
        readline.add_history(inp)
        self._input_queue.append(inp)

    def interactive(self):
        """
        Start the interactive session
        """
        self._interactive_interact()
        back_from_interactive = False
        while True:
            if back_from_interactive:
                self.back_from_interactive = False
                print(self.last_received.decode("latin1"), end="")
                self._handle_input()
                continue
            try:
                rcvd = b""
                self.last_received = rcvd
                while (rcvd:=self.r.recv(timeout=0.1)) != b"":
                    self.last_received += rcvd
                print(self.last_received.decode("latin1"), end="")
                self._handle_input()
            except EOFError:
                print(f"EOFError: Exiting. Last received: {self.last_received.decode('latin1')}")
                exit(0)

    def _help_command(self, _: list[str]) -> bool:
        """
        Command name: h
        Description: Display available commands and important variables

        Usage: !h
        """
        print("Available commands:")
        for k, v in self._commands.items():
            print(f"{self._command_prefix()}{k}: {" ".join(v.__name__.split('_')[1:])}")
            if v.__doc__ is not None:
                print(f"Description: {v.__doc__}")
        print("")
        print("Important variables:")
        print(f"{self._command_prefix()}last_eval_res: Last result of an eval command")
        return True

    def _pid_command(self, _: list[str]) -> bool:
        """
        Command name: pid
        Description: Display the PID of the process

        Usage: !pid
        """
        print(f"PID: {self.r.pid}")
        return True

    def _quit_command(self, _: list[str]) -> bool:
        """
        Command name: q
        Description: Exit the program

        Usage: !q
        """
        print("Exiting")
        self.r.close()
        exit(0)

    def _handle_input(self):
        inp = input() if len(self._input_queue) == 0 else self._input_queue.pop(0)
        if inp == f"{self._command_prefix()}i":
            print("Entering interactive mode")
            self._interactive_interact()
            self.back_from_interactive = True
            return
        if (
            inp[: len(self._command_prefix())] == self._command_prefix()
            and inp[len(self._command_prefix()) :] in self.vars
        ):
            inp = self.vars[inp[len(self._command_prefix()) :]].decode("latin1")
        if inp == "" or inp[-1] != "\n":
            inp += "\n"
        self.r.send(inp.encode("latin1"))

    def _interactive_interact(self):
        while True:
            command = (
                input() if len(self._input_queue) == 0 else self._input_queue.pop(0)
            )
            command, params = self._parse_command(command.split(" "))
            if command is None:
                print("Invalid command")
                continue
            res = command(params)
            if not res:
                break

    def _eval_command(self, args: list[str]) -> bool:
        """
        Command name: e
        Description: Evaluate an expression and store the result in last_eval_res

        Usage: !e expression
        """
        if len(args) < 1:
            print("Invalid number of arguments")
            return True

        res = eval(" ".join(args), globals(), self.vars)
        print(f"Evaluated: {' '.join(args)} to {res}")
        self.vars["last_eval_res"] = (
            str(res).encode() if not isinstance(res, bytes) else res
        )

        return True

    def _copy_command(self, args: list[str]) -> bool:
        """
        Command name: c
        Description: Copy a variable to another

        Usage: !c var_name new_name
        """
        if len(args) != 2:
            print("Invalid number of arguments")
            return True
        var_name = args[0]
        new_name = args[1]
        if var_name not in self.vars:
            print(f"Variable {var_name} not found")
            return True
        print(f"Copying {var_name} to {new_name}")
        self.vars[new_name] = self.vars[var_name]
        return True

    def _back_command(self, args: list[str]) -> bool:
        """
        Command name: b
        Description: Exit interactive mode

        Usage: !b
        """
        print("Exiting interactive mode")
        print("Last received:")
        print(self.last_received.decode("latin1"))
        return False

    def _add_command(self, args: list[str]) -> bool:
        """
        Command name: +
        Description: Add two variables and store the result in another

        Usage: !+ var1 var2 result
        """
        if len(args) != 3:
            print("Invalid number of arguments")
            return True
        v1 = args[0]
        v2 = args[1]
        res = args[2]
        if v1 not in self.vars:
            print(f"Variable {v1} not found")
            return True
        if v2 not in self.vars:
            print(f"Variable {v2} not found")
            return True
        if not is_numeric(self.vars[v1]) or not is_numeric(self.vars[v2]):
            print(f"Invalid arguments: {v1} or {v2} are not numeric")
            return True
        print(
            f"Adding {self.vars[v1]} and {self.vars[v2]} to {res} (result: {int(self.vars[v1]) + int(self.vars[v2])})"
        )
        self.vars[res] = str(int(self.vars[v1]) + int(self.vars[v2])).encode()
        return True

    def _sub_command(self, args: list[str]) -> bool:
        """
        Command name: -
        Description: Subtract two variables and store the result in another

        Usage: !- var1 var2 result
        """
        if len(args) != 3:
            print("Invalid number of arguments")
            return True
        v1 = args[0]
        v2 = args[1]
        res = args[2]
        if v1 not in self.vars:
            print(f"Variable {v1} not found")
            return True
        if v2 not in self.vars:
            print(f"Variable {v2} not found")
            return True
        if not is_numeric(self.vars[v1]) or not is_numeric(self.vars[v2]):
            print(f"Invalid arguments: {v1} or {v2} are not numeric")
            return True
        print(
            f"Subtracting {self.vars[v1]} and {self.vars[v2]} to {res} (result: {int(self.vars[v1]) - int(self.vars[v2])})"
        )
        self.vars[res] = str(int(self.vars[v1]) - int(self.vars[v2])).encode()
        return True

    def _mul_command(self, args: list[str]) -> bool:
        """
        Command name: *
        Description: Multiply two variables and store the result in another

        Usage: !* var1 var2 result
        """
        if len(args) != 3:
            print("Invalid number of arguments")
            return True
        v1 = args[0]
        v2 = args[1]
        res = args[2]
        if v1 not in self.vars:
            print(f"Variable {v1} not found")
            return True
        if v2 not in self.vars:
            print(f"Variable {v2} not found")
            return True
        if not is_numeric(self.vars[v1]) or not is_numeric(self.vars[v2]):
            print(f"Invalid arguments: {v1} or {v2} are not numeric")
            return True

        print(
            f"Multiplying {self.vars[v1]} and {self.vars[v2]} to {res} (result: {int(self.vars[v1]) * int(self.vars[v2])})"
        )
        self.vars[res] = str(int(self.vars[v1]) * int(self.vars[v2])).encode()
        return True

    def _div_command(self, args: list[str]) -> bool:
        """
        Command name: /
        Description: Divide two variables and store the result in another

        Usage: !/ var1 var2 result
        """
        if len(args) != 3:
            print("Invalid number of arguments")
            return True
        v1 = args[0]
        v2 = args[1]
        res = args[2]
        if v1 not in self.vars:
            print(f"Variable {v1} not found")
            return True
        if v2 not in self.vars:
            print(f"Variable {v2} not found")
            return True
        if (
            not is_numeric(self.vars[v1])
            or not is_numeric(self.vars[v2])
            or int(self.vars[v2]) == 0
        ):
            print(f"Invalid arguments: {v1} or {v2} are not numeric or {v2} is 0")
            return True

        print(
            f"Dividing {self.vars[v1]} and {self.vars[v2]} to {res} (result: {int(self.vars[v1]) / int(self.vars[v2])})"
        )
        self.vars[res] = str(int(self.vars[v1]) / int(self.vars[v2])).encode()
        return True

    def _append_command(self, args: list[str]) -> bool:
        """
        Command name: a
        Description: Append two variables and store the result in another

        Usage: !a var1 var2 result
        """
        if len(args) != 3:
            print("Invalid number of arguments")
            return True
        v1 = args[0]
        v2 = args[1]
        res = args[2]
        if v1 not in self.vars:
            print(f"Variable {v1} not found")
            return True
        if v2 not in self.vars:
            print(f"Variable {v2} not found")
            return True

        print(
            f"Appending {self.vars[v1]} and {self.vars[v2]} to {res} (result: {self.vars[v1] + self.vars[v2]})"
        )
        self.vars[res] = self.vars[v1] + self.vars[v2]
        return True

    def _slice_command(self, args: list[str]) -> bool:
        """
        Command name: sl
        Description: Slice a variable and store the result in another

        Usage: !sl var start end result
        """
        if len(args) != 4:
            print("Invalid number of arguments")
            return True
        v1 = args[0]
        start = args[1]
        end = args[2]
        res = args[3]
        if v1 not in self.vars:
            print(f"Variable {v1} not found")
            return True
        if not start.isnumeric() or not end.isnumeric():
            print(f"Invalid arguments: {start} or {end} are not numeric")
            return True

        print(
            f"Slicing {self.vars[v1]} from {start} to {end} to {res} (result: {self.vars[v1][int(start) : int(end)]})"
        )
        self.vars[res] = self.vars[v1][int(start) : int(end)]
        return True

    def _store_command(self, args: list[str]) -> bool:
        """
        Command name: s
        Description: Store a line or part of a line in a variable

        Usage: !s all var_name
        Usage: !s line range|all var_name
        """
        if len(args) < 2:
            print("Invalid number of arguments")
            return True
        var_name = args[-1]
        line_arg = args[0]
        range_arg = args[1]
        last_received = self.last_received.decode("latin1")
        if line_arg == "all":
            print(f"Storing all to {var_name}")
            self.vars[var_name] = last_received.encode()
            return True
        line_to_save = 0
        if not is_numeric(line_arg):
            print(f"Invalid LINE argument: {line_arg}")
            return True
        line_to_save = int(line_arg)
        line = last_received.split("\n")[line_to_save]

        if range_arg == "all":
            print(f"Storing {line} to {var_name}")
            self.vars[var_name] = line.encode()
            return True

        if range_arg.count("-") != 1 and not is_numeric(range_arg):
            print(f"Invalid RANGE argument: {range_arg}")
            return True
        if is_numeric(range_arg):
            self.vars[var_name] = line[int(range_arg)].encode()
            return True

        range_start, range_end = range_arg.split("-")
        if not range_start.isnumeric() or not range_end.isnumeric():
            print(f"Invalid RANGE argument: {range_arg}")
            return True

        print(f"Storing {line[int(range_start) : int(range_end)]} to {var_name}")
        self.vars[var_name] = line[int(range_start) : int(range_end)].encode()
        return True

    def _add_var_command(self, args: list[str]) -> bool:
        """
        Command name: v
        Description: Add a variable

        Usage: !v var_name value
        """
        if len(args) != 2:
            print("Invalid number of arguments")
            return True
        var_name = args[0]
        value = args[1]
        print(f"Adding {value} to {var_name}")
        self.vars[var_name] = value.encode()
        return True

    def _dump_vars_command(self, args: list[str]) -> bool:
        """
        Command name: d
        Description: Dump all variables

        Usage: !d [latin1|hex]
        """
        display_fmt = args[0] if len(args) > 0 else "latin1"
        if display_fmt not in ["latin1", "hex"]:
            print("Invalid display format")
            return True

        print("Dumping variables")
        if display_fmt == "hex":
            for k, v in self.vars.items():
                print(f"{k}: {str(v)[2:-1]}")
            return True

        for k, v in self.vars.items():
            print(f"{k}: {v.decode("latin1")}")
        return True

    def _print_last_received_command(self, _: list[str]) -> bool:
        """
        Command name: p
        Description: Print the last received data

        Usage: !p
        """
        splited = self.last_received.split(b"\n")
        for i, line in enumerate(splited):
            print(f"{i:03}: {line.decode("latin1")}")
        return True

    def _hex_command(self, args: list[str]) -> bool:
        """
        Command name: 16
        Description: Convert a variable to hex

        Usage: !16 var_name
        """
        if len(args) != 1:
            print("Invalid number of arguments")
            return True
        var_name = args[0]
        if var_name not in self.vars:
            print(f"Variable {var_name} not found")
            return True
        print(f"Converting {var_name} to hex")
        self.vars[var_name] = hex(int(self.vars[var_name])).encode()
        return True

    def _dec_command(self, args: list[str]) -> bool:
        """
        Command name: 10
        Description: Convert a variable to decimal

        Usage: !10 var_name
        """
        if len(args) != 1:
            print("Invalid number of arguments")
            return True
        var_name = args[0]
        if var_name not in self.vars:
            print(f"Variable {var_name} not found")
            return True
        print(f"Converting {var_name} to decimal")
        self.vars[var_name] = str(int(self.vars[var_name], 16)).encode()
        return True

    def _parse_command(self, command: list[str]):
        cmd = command[0]
        args = command[1:]
        if cmd[0 : len(self._command_prefix())] != self._command_prefix():
            return (None, [])
        cmd = cmd[len(self._command_prefix()) :]
        return (self._commands.get(cmd, None), args)


def is_numeric(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False
