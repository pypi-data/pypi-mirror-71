Flash messaging for fresco web applications
===========================================

fresco-flash provides a mechanism for displaying messages to end users in a web
application. Messages can be sent across requests: you can generate a message
in a view that returns a redirect response and the message will display on
the next page loaded.

Example usage::


    from fresco import FrescoApp
    from fresco_flash import FlashMiddleware, flash

    # Create a fresco app with the flash messaging middleware enabled
    app = FrescoApp()
    app.add_middleware(FlashMiddleware)

    # Create some flash messages to be shown to the user
    flash.info('Thanks for signing up!')
    flash.warn('Did you remember to feed the cat?')
    flash.error('Too many elephants: increase bun supply before proceeding.')

    # Display messages to the user
    <py:for each="level, item in flash.messages()">
        <div class="message $level">$item</div>
    </py:for>


Including HTML in messages
--------------------------

Messages are automatically escaped for HTML using
MarkupSafe_.
If you want to include unescaped HTML in flash messages, wrap them in
`markupsafe.Markup` first::

    from markupsafe include Markup

    flash.info(Markup('<blink>Insert coin for new game</blink>'))

.. _MarkupSafe: https://pypi.python.org/pypi/MarkupSafe
