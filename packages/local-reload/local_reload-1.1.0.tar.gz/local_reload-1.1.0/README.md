# local_reload

Provides a means of identifying and automatically reloading "stale" pages. 

Keeps a "last update time" in localStorage, and updates it whenever the user "updates data". Any time the user "returns" to a page (via browser history, or switches tabs/windows), that page will automatically reload if it is stale (if it was rendered before the last update time).

Intended for use on CRUD heavy sites, especially when you use history.back() or use multiple tabs/windows as part of the normal workflow.

## Limitations

### Update Time is Per-Browser

If data is updated in one browser, it will not reload pages in another browser. This is designed for a single user updating and viewing data in a single browser. We use `window.localStorage` to store the update time, so our scope is the same as that of localStorage (hence the name "local_reload").

### Update Time is Site-Wide

A single, site-wide "update time" is maintained. A change in one piece of data will invalidate all previously rendered pages, even if they do not display that data.

### Update Detection

We automatically reset the update time when any form is POSTed. To be more precise - we reset the update time on every form submit event, as long as the form's method is not GET.

This works well if you use actual form submissions (even if handled via javascript) as the event which triggers data updates. If you update data without the user submitting a form, then you must manually call `window.local_reload_invalidate()`.

### No Background Reload

Pages will not be reloaded in background tabs/windows. They will only be reloaded when the user returns focus to them. This is actually by design. Previous attempts to reload background windows/tabs resulted in undesirable behaviour in many situations.

## Installation

- `pip install local_reload`
- add 'local_reload' to `INSTALLED_APPS`
- `{% include "local_reload/local_reload_support.html" %}` in the `head`<sup>\*</sup> of any page that displays or updates data

<sup>\*</sup> This should be added near the top of your `head`, so it can run as early as possible.

## NavTricks

We include a copy of NavTricks.js in our static files. This script pairs perfectly with local_reload. 
