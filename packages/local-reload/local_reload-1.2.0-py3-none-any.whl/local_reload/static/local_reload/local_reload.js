'use strict';
(function() {
    // Make available globally, so users can call manually if needed
    window.local_reload_invalidate = function() {
        localStorage.local_reload_update_time = Date.now();
    }
    // Users can set this true to temporarily disable local_reload
    window.disable_local_reload = false;

    // Call whenever user submits a non-GET form
    addEventListener('submit', function(e) {
        if (e.target.method != 'get') local_reload_invalidate();
    });

    function reload_if_necessary(erasing_document) {
        if (window.disable_local_reload) return

        var last_update = localStorage.local_reload_update_time;
        if (!last_update) return

        var rendered = document.getElementById('local_reload_timestamp').getAttribute('data-rendered');
        if (rendered > last_update) return // page is not stale

        /*
            Sometimes it makes sense to erase the page content, 
            so that the user doesn't see the stale content while the fresh content loads.
        */
        if (erasing_document) {
            document.documentElement.innerHTML = '';            
        }

        window.location.reload();
    }
    var reload_if_necessary_erasing = reload_if_necessary.bind(null, true);
    
    /*
        Check now (in case page was loaded from http cache),
        and on pageshow (in case page is loaded from in-memory "bfcache").
    
        In these cases, erase the document's content immediately,
        so that the user doesn't see it while the page reloads.

        This window is navigating from another page, 
        and it looks weird to load/display the stale data for a split second.
    */
    reload_if_necessary_erasing();
    addEventListener('pageshow', reload_if_necessary_erasing);

    /*
        Check on visibilitychange (when the user switches tabs),
        and on window focus (when the user switches windows).

        Since the user knowingly had the stale document open in another tab/window,
        let the user see that data immediately. 

        Do not clear document content before reloading.
    */
    document.addEventListener('visibilitychange', reload_if_necessary);
    addEventListener('focus', reload_if_necessary_erasing);
})();