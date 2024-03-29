var versions = ["dev", "0.1.x"];

function insert_version_links() {
    for (i = 0; i < versions.length; i++) {
        open_list = "<li>";
        if (typeof DOCUMENTATION_OPTIONS !== "undefined") {
            if (
                DOCUMENTATION_OPTIONS["VERSION"] == versions[i] ||
                (DOCUMENTATION_OPTIONS["VERSION"].match(/dev$/) && i == 0)
            ) {
                open_list = '<li id="current">';
            }
        }
        document.write(open_list);
        document.write(
            '<a href="URL">pysarpro VERSION</a> </li>\n'
                .replace("VERSION", versions[i])
                .replace(
                    "URL",
                    "https://pol-insar.github.io/docs/" + versions[i]
                )
        );
    }
}

function stable_version() {
    return versions[1];
}
