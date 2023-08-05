Single and multiple line status updates with minimal update sequences.

*Latest release 20200613*:
* New UpdProxy.__call__ which sets the .text property in the manner of logging calls, with (msg,*a).
* New Upd.normalise static method exposing the text normalisation `unctrl(text.rstrip())`.
* New UpdProxy.prefix attribute with a fixed prefix for status updates; `prefix+text` is left cropped for display purposes when updated.
* New UpdProxy.width property computing the space available after the prefix, useful for sizing things like progress bars.
* Make UpdProxy a context manager which self deletes on exit.
* Upd: make default backend=sys.stderr, eases the common case.
* New Upd.above() context manager to support interleaving another stream with the output, as when stdout (for print) is using the same terminal as stderr (for Upd).
* New out() top level function for convenience use with the default Upd().
* New nl() top level function for writing a line to stderr.
* New print() top level function wrapping the builtin print; callers can use "from cs.upd import print" to easily interleave print() with cs.upd use.

This is available as an output mode in `cs.logutils`.

Single line example:

    from cs.upd import Upd, nl, print
    .....
    with Upd() as U:
        for filename in filenames:
            U.out(filename)
            ... process filename ...
            U.nl('an informational line to stderr')
            print('a line to stdout')

Multiline multithread example:

    from threading import Thread
    from cs.upd import Upd, print
    .....
    def runner(filename, proxy):
        # initial status message
        proxy.text = "process %r" % filename
        ... at various points:
            # update the status message with current progress
            proxy.text = '%r: progress status here' % filename
        # completed, remove the status message
        proxy.close()
        # print completion message to stdout
        print("completed", filename)
    .....
    with Upd() as U:
        U.out("process files: %r", filenames)
        Ts = []
        for filename in filenames:
            proxy = U.insert(1) # allocate an additional status line
            T = Thread(
                "process "+filename,
                target=runner,
                args=(filename, proxy))
            Ts.append(T)
            T.start()
        for T in Ts:
            T.join()

## Function `cleanupAtExit()`

Cleanup function called at programme exit to clear the status line.

## Function `nl(msg, *a, **kw)`

Write `msg` to `file` (default `sys.stdout`),
without interfering with the `Upd` instance.
This is a thin shim for `Upd.print`.

## Function `out(msg, *a, **outkw)`

Update the status line of the default `Upd` instance.
Parameters are as for `Upd.out()`.

## Function `print(*a, **kw)`

Wrapper for the builtin print function
to call it inside `Upd.above()` and enforce a flush.

The function supports an addition parameter beyond the builtin print:
* `upd`: the `Upd` instance to use, default `Upd()`

Programmes intregrating `cs.upd` with use of the builtin `print`
function should use this as import time:

    from cs.upd import print

## Class `Upd(cs.obj.SingletonMixin)`

A `SingletonMixin` subclass for maintaining a regularly updated status line.

The default backend is `sys.stderr`.

## Class `UpdProxy`

A proxy for a status line of a multiline `Upd`.

This provides a stable reference to a status line after it has been
instantiated by `Upd.insert`.

The status line can be accessed and set via the `.text` property.

An `UpdProxy` is also a context manager which self deletes on exit:

    U = Upd()
    ....
    with U.insert(1, 'hello!') as proxy:
        .... set proxy.text as needed ...
    # proxy now removed

# Release Log



*Release 20200613*:
* New UpdProxy.__call__ which sets the .text property in the manner of logging calls, with (msg,*a).
* New Upd.normalise static method exposing the text normalisation `unctrl(text.rstrip())`.
* New UpdProxy.prefix attribute with a fixed prefix for status updates; `prefix+text` is left cropped for display purposes when updated.
* New UpdProxy.width property computing the space available after the prefix, useful for sizing things like progress bars.
* Make UpdProxy a context manager which self deletes on exit.
* Upd: make default backend=sys.stderr, eases the common case.
* New Upd.above() context manager to support interleaving another stream with the output, as when stdout (for print) is using the same terminal as stderr (for Upd).
* New out() top level function for convenience use with the default Upd().
* New nl() top level function for writing a line to stderr.
* New print() top level function wrapping the builtin print; callers can use "from cs.upd import print" to easily interleave print() with cs.upd use.

*Release 20200517*:
* Multiline support!
* Multiline support!
* Multiline support!
* New UpdProxy class to track a status line of a multiline Upd in the face of further inserts and deletes.
* Upd(...) now returns a context manager to clean up the display on its exit.
* Upd(...) is now a SingletonMixin in order to use the same state if set up in multiple places.

*Release 20200229*:
* Upd: can now be used as a context manager, clearing the line on exit.
* Upd.without is now a context manager, returning the older state, and accepting an optional inner state (default "").
* Upd is now a singleton factory, obsoleting upd_for.
* Upd.nl: use "insert line above" mode if supported.

*Release 20181108*:
Documentation improvements.

*Release 20170903*:
* New function upd_for(stream) returning singleton Upds.
* Drop noStrip keyword argument/mode - always strip trailing whitespace.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* Add Upd.flush method.
* Upd.out: fix longstanding trailing text erasure bug.
* Upd.nl,out: accept optional positional parameters, use with %-formatting if supplied, just like logging.

*Release 20150118*:
metadata fix

*Release 20150116*:
Initial PyPI release.
