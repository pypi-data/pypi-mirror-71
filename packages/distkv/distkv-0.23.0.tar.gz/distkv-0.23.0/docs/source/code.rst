==============
Code in DistKV
==============

DistKV can store Python code and modules, either for direct use by your
client or for a runner daemon.

TODO: There is no dependency resolution. Thus, while you can store Python
modules in DistKV, there's no guarantee yet that they'll actually be present
when your code loads.


++++
Code
++++

Python code stored in DistKV is wrapped with a procedure context, mainly to
make returning a result more straightforward. This is done by indenting the
code before compiling it: don't depend on multi-line strings to be flush
left.

Storage
=======

The location for executable scripts is configurable and defaults to
".distkv code proc". Scripts are stored as a dict with these attributes:

* ``code``: the actual text

* ``is_async``: a flag whether the procedure is synchronous (``None``),
  sync but should run in a worker thread (``False``), or async (``True``).

* ``vars``: Required input variables of your procedure. Parameters not
  mentioned here are still available as globals.

* ``requires``: modules which this code needs.  XXX TODO

There's no way for code written for a specific async library to run under
another, with the possible exception of "asyncio on top of Trio" (via
``trio-asyncio``). DistKV itself uses ``anyio`` in order to avoid the
problem. The author strongly recommends to follow this practice, if at all
possible.

The required modules must be stored in DistKV. Accessing modules from your
Python installation or the virtualenv you've set up for DistKV is of course
possible, but DistKV does not try to keep them up-to-date for you.

If you want to run user code in your DistKV module, call
``cr = await CodeRoot.as_handler(client)``. Then, run some code by
simply naming it: ``cr("forty.two")`` or ``cr(("forty","two"))`` will run
the code stored at ``.distkv code proc forty two``. All arguments will be
passed to the stored code.


+++++++
Modules
+++++++

Python modules are stored to DistKV as plain code.

Recursive dependencies are not allowed.

Storage
=======

The location for Python modules is configurable and defaults to
".distkv code module". Modules are stored as a dict with these attributes:

* ``code``: the actual program text

* ``requires``: other modules which this module needs to be loaded.

Usage
=====

Call ``await ModuleRoot.as_handler(client)``. All modules in your DistKV
store are loaded into the Python interpreter; use normal import statements
to access them.

TODO: Modules are not yet loaded incrementally.


+++++++
Runners
+++++++

The distributed nature of DistKV lends itself to running arbitrary code on
any node that can accomodate it. 

============
Runner types
============

DistKV has three built-in types of code runners. All are organized by a "group"
tag. The "distkv client run all" command starts all jobs of a type, in a
specific group.

Single-node runner
==================

This runner executes code on a specific node. This is useful e.g. if you
need to access actual hardware.

Any-node runner
===============

This runner executes code on one of a group of nodes. Which node executes
the code is largely determined by chance, startup order, or phase of the
moon.

TODO: Load balancing is not yet implemented.

All nodes in a runner form an Actor group; the node that holds the Tag
checks whether jobs need to start.

All-node runner
===============

This runner executes code on all members of a group of nodes.

====================
Runner configuration
====================

Runner entries don't hold code; they merely point to it. The advantage is
that you can execute the same code with different parameters.

See :class:`distkv.runner.RunnerEntry` for details.

The actual runtime information is stored in a separate "state" node.
This avoids race conditions.
See :class:`distkv.runner.StateEntry` for details.

Variables
=========

The runners pass a couple of variables to their code.

* _entry

  The current runner entry. Try not to modify it.

* _client

  The DistKV client instance.

* _cfg

  The current configuration.

* _info (async only)

  A queue for events. Currently, receives subclasses of
  :cls:`asyncactor.ActorState`, to signal whether the running node is
  connected to any / all of your DistKV-using infrastructure.

These are available as global variables.

Node Groups
===========

All runners are part of a group of nodes. The Any-Node runners use the
group to synchronize job startup.

Runners also forward the group's membership information to your code as it
changes. You can use this information to implement "emergency operation
when disconnected" or similar fallback strategies.

