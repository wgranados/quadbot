import pytest
from commands import Command
from plugins.Send import Send
from plugins.Credits import Credits
from plugins.math.Latex import Latex
from plugins.math.Calculator import Calculator
from plugins.math.Putnam import Putnam
from plugins.Machine import Machine
from plugins.Xkcd import Xkcd
from plugins.Dilbert import Dilbert
from plugins.PartyParrot import PartyParrot
from plugins.Broadcast import Broadcast


from room import Room
from user import User
from robot import ReplyObject


test_room = Room('test')
test_user = User('user')
test_owner = User('user', ' ', True)


@pytest.fixture
def before():
    global test_user
    global test_room
    global test_owner
    test_user = User('test')
    test_room = Room('test')
    test_owner = User('test', ' ', True)


def test_commands_delegation():
    cmd_out = Command(None, 'send', test_room, 'testing', test_owner)
    answer = ReplyObject('testing', True, True)
    assert cmd_out == answer, "delegation to modules doesn't work"

    cmd_out = Command(None, 'machine', test_room, '', test_user)
    answer = ReplyObject('I am the machine!', True)
    assert cmd_out == answer, "delegation to modules doesn't work"

    cmd_out = Command(None, 'secret', test_room, '', test_owner)
    answer = ReplyObject('This is a secret command!', True)
    assert cmd_out == answer, "delegation to secret commands doesn't work"


def test_send():
    cmd = Send()

    reply = cmd.response(test_room, test_user, ['hi'])
    answer = ReplyObject("This command is reserved for this bot's owner", True)
    assert reply == answer, 'send command does not handle permissions correctly'

    reply = cmd.response(test_room, test_owner, ['hi'])
    answer = ReplyObject('hi', True, True)
    assert reply == answer, "send command's success output is incorrect"

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject('Responds with arguments passed to this command, reserved for bot owner', True)
    assert reply == answer, "send command's help output incorrect"


def test_credits():
    cmd = Credits()

    reply = cmd.response(test_room, test_user, [])
    answer = ReplyObject("Source code can be found at: https://github.com/wgma00/quadbot/", True)
    assert reply == answer, "Credit command's success output is incorrect"

    reply = cmd.response(test_room, test_owner, ['arg1', 'arg2'])
    answer = ReplyObject("This command doesn't take any arguments", True)
    assert reply == answer, "Credit command shouldn't take any arguments"

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject("Responds with url to this bot's source code", True)
    assert reply == answer, "Credit command's help output incorrect"


def test_latex():
    cmd = Latex()

    reply = cmd.response(test_room, test_user, [])
    answer = ReplyObject("Insufficient arguments provided. Should have a LaTeX expression surrounded by $.\n", True)
    assert reply == answer, 'insufficient arguments not handled correctly'

    reply = cmd.response(test_room, test_user, ['$1+1$'])
    assert reply.text.startswith('http'), "Compiling and/or uploading to imgur doesn't work"

    test_room.rank = '*'
    reply = cmd.response(test_room, test_user, ['$1+1$', 'showimage'])
    assert 'http' in reply.text, "Compiling, showimaging, and/or  uploading to imgur doesn't work"

    test_room.rank = ' '
    reply = cmd.response(test_room, test_user, ['$1+1$', 'showimage'])
    answer = ReplyObject('This bot requires * or # rank to showimage in chat', True)
    assert reply == answer, "Showimages with insufficient privileges not handled correctly"

    reply = cmd.response(test_room, test_user, ['$\\begin{}+1$'])
    answer = ReplyObject('There was an internal error. Check your LaTeX expression for any errors', True)
    assert reply == answer, "Exceptions aren't handled correctly"

    reply = cmd.response(test_room, test_user, '$\input{/etc/passwd}$')
    answer = ReplyObject(('You have inputted an invalid LaTeX expression. You may have forgotten to surround '
                          'your expression with $. Or you may have used restricted LaTeX commands'), True)
    assert reply == answer, 'Dangerous input not handled correctly'

    reply = cmd.response(test_room, test_owner, ['tikz-cd', 'addpackage'])
    answer = ReplyObject('tikz-cd has been added. This is not saved on restart', True, True)
    assert reply == answer, 'addpackage functionality not working'

    reply = cmd.response(test_room, test_owner, ['tiks-cd', 'addpackage'])
    answer = ReplyObject(('You may only install one package at a time. i.e. latex tikz-cd, addpackage . If that '
                          'is not the issue then it is possible that the package specified is not available on '
                          'the host system'), True)
    assert reply == answer, 'addpackage package installation error not correct'

    reply = cmd.response(test_room, test_user, ['tikz-cd', 'addpackage'])
    answer = ReplyObject('This command is reserved for RoomOwners', True)
    assert reply == answer, 'addpackage functionality not working'

    test_room.isPM = True
    reply = cmd.response(test_room, test_user, ['$1+1$', 'showimage'])
    answer = ReplyObject('This bot cannot showimage in PMs.', True)
    assert reply == answer, 'Showimages in PMs not handled correctly'
    test_room.isPm = False


def test_machine():
    cmd = Machine()

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject("Responds with I am the machine! [[The Machine - Bert Kreischer: THE MACHINE]]", True)
    assert reply == answer, "Help command output isn't correct"

    reply = cmd.response(test_room, test_user, ["whodamachine?"])
    answer = ReplyObject("This command doesn't take any arguments", True)
    assert reply == answer, "Help command Amount of arguments taken is incorrect"

    reply = cmd.response(test_room, test_user, [])
    answer = ReplyObject("I am the machine!", True)
    assert reply == answer, "Help command success output not correct"


def test_calc():
    cmd = Calculator()

    # generic test
    reply = cmd.response(test_room, test_user, ['1+1'])
    answer = ReplyObject('2', True)
    assert reply == answer, 'incorrect arithmetic expression'

    # testing for substitution
    reply = cmd.response(test_room, test_user, ['|sin(-x)|', '0'])
    answer = ReplyObject('0', True)
    assert reply == answer, 'incorrect arithmetic expression'

    # testing for singular substitution
    reply = cmd.response(test_room, test_user, ['x'])
    answer = ReplyObject('0', True)
    assert reply == answer, 'incorrect arithmetic expression'

    # testing on a relatively large factorial
    reply = cmd.response(test_room, test_user, ['191!'])
    answer = ReplyObject('1.848941631×10³⁵⁴', True)
    assert reply == answer, 'incorrect arithmetic expression'

    # testing on incorrect input
    reply = cmd.response(test_room, test_user, [])
    answer = ReplyObject('There should be an expression optionally followed by substitution', True)
    assert reply == answer, 'invalid expression recognized by calculator'

    # break out of the echo '' by completing the ', then do some nasty things
    reply = cmd.response(test_room, test_user, ["'rm"])
    answer = ReplyObject('invalid input', True)
    assert reply == answer, 'dangerous user input not handled correctly'

    reply = cmd.response(test_room, test_user, ["$'rm"])
    answer = ReplyObject('invalid input', True)
    assert reply == answer, 'dangerous user input not handled correctly'

    reply = cmd.response(test_room, test_user, ["1+test"])
    answer = ReplyObject('invalid input', True)
    assert reply == answer, 'dangerous user input not handled correctly'


def test_xkcd():
    cmd = Xkcd()

    reply = cmd.response(test_room, test_user, [])
    assert reply.text.startswith('https'), "xkcd command proper url isn't sent"

    reply = cmd.response(test_room, test_user, ['1'])
    answer = ReplyObject('https://imgs.xkcd.com/comics/barrel_cropped_(1).jpg', True)
    assert reply == answer, 'xkcd command individual xkcd article not found'

    reply = cmd.response(test_room, test_user, ['rand'])
    assert reply.text.startswith('https'), 'xkcd command rand xkcd article not found'

    test_room.rank = '*'
    reply = cmd.response(test_room, test_user, ['rand', 'showimage'])
    assert reply.text.startswith('/addhtmlbox'), 'xkcd command rand showimage xkcd article not found'
    test_room.rank = ' '

    test_room.rank = '*'
    reply = cmd.response(test_room, test_user, ['showimage'])
    assert reply.text.startswith('/addhtmlbox'), 'xkcd command recent showimage xkcd article not found'
    test_room.rank = ' '

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject(("Responds with url to xkcd article. if left empty, returns most recent. If 'rand' is passed generates a random article. "
                          "If a 'number' is passed, returns that specified xkcd article. This command also supports showimages."), True)
    assert reply == answer, 'xkcd command help function is incorrect'


def test_dilbert():
    cmd = Dilbert()

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject(("Responds with url to random xkcd article, number can also be specified. And this command "
                          "supports showimages."), True)
    assert reply == answer, 'Help command for Dilbert is incorrect'

    reply = cmd.response(test_room, test_user, [])
    assert reply.text.startswith('http'), 'Dilbert command url not generated.'

    reply = cmd.response(test_room, test_user, ['args1', 'args2'])
    answer = ReplyObject("This command doesn't take any arguments", True)
    assert reply == answer, 'arguments passed to Dilbert command when they should not'


def test_parrot():
    cmd = PartyParrot()

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject(('If left empty prints a url to a random parrot from http://cultofthepartyparrot.com/, '
                          'otherwise you may choose to print a specific url. This command supports showimages.'), True)
    assert reply == answer, 'help for party parrot is not correct'

    reply = cmd.response(test_room, test_user, ['sirocco'])
    answer = ReplyObject('http://cultofthepartyparrot.com/assets/sirocco.gif', True)
    assert reply == answer, 'stuff'

    reply = cmd.response(test_room, test_user, ['sirocco', 'showimage'])
    answer = ReplyObject('This bot requires * or # rank to showimage in chat', True)
    assert reply == answer, 'stuff'

    test_room.rank = '*'
    reply = cmd.response(test_room, test_user, ['sirocco', 'showimage'])
    assert reply.text.startswith('/addhtmlbox'), 'stuff'


def test_putnam_problem():
    cmd = Putnam()

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject('This generates a link to a random putnam problem from {start} to {end} and supports showimages'.format(start=1985, end=2016), True)
    assert reply == answer, 'help output for putnam problem is incorrect.'

    test_room.rank = '*'
    test_room.isPM = False
    reply = cmd.response(test_room, test_user, ['showimage'])
    assert reply.text.startswith('/addhtmlbox'), "show imaging doesn't work in putnam_problem"


def test_broadcast():
    cmd = Broadcast()

    reply = cmd.response(test_room, test_user, ['help'])
    answer = ReplyObject(("If no arguments are passed, display current broadcast rank."
                          " Otherwise you can provide one of the following arguments: "
                          "off, +, %, @, *, #. This doesn't work in Pms."), True)
    assert reply == answer, "Broadcast command's help command is incorrect"

    reply = cmd.response(test_room, test_user, ['+'])
    answer = ReplyObject('This command is reserved for Room Owners(#)', True)
    assert reply == answer, "Broadcast rank checking is incorrect"

    test_user.rank = '#'  # Make this user a room owner
    reply = cmd.response(test_room, test_user, ['+'])
    answer = ReplyObject('Broadcast rank set to +. (This is not saved on reboot)', True)
    assert reply == answer, "Broadcast rank setting output is incorrect"
    test_user.rank = ' '

    reply = cmd.response(test_room, test_owner, ['+'])
    answer = ReplyObject('Broadcast rank set to +. (This is not saved on reboot)', True)
    assert reply == answer, "Broadcast rank setting output is incorrect"

    reply = cmd.response(test_room, test_owner, ['test'])
    answer = ReplyObject('You have provided an invalid argument', True)
    assert reply == answer, "Broadcast command is not detecting incorrect ranks correctly"

    reply = cmd.response(test_room, test_owner, ['arg1', 'arg2'])
    answer = ReplyObject('This command only takes 1 argument', True)
    assert reply == answer, "Broadcast command is not handling amount of arguments correctly"

    test_room.isPM = True
    reply = cmd.response(test_room, test_owner, ['+'])
    answer = ReplyObject('There are no broadcast ranks in PMs', True)
    assert reply == answer, "Broadcast command is handling PM commands incorrectly"
