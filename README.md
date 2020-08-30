# Reaktor pre-assignment
A small program written in Python, using Flask, that exposes some key information about software packages known to a Debian/Ubuntu system via an HTML interface.
* The index page lists installed packages alphabetically with package names as links.
* When following each link, you arrive at a piece of information about a single package. The following information is included:
    * Name
    * Description
    * The names of the packages the current package depends on (version skipped)
    * Reverse dependencies, i.e. the names of the packages that depend on the current package

* The dependencies and reverse dependencies are clickable and the user can navigate the package structure by clicking from package to package. Sometimes there are alternates in a dependency list, separated by the pipe character |. When rendering such dependencies, alternatives that map to package names that have entries in the file are rendered as a links. For thise that don't, the name is simply printed out.
* The program is running on Heroku [here](https://pm-reaktor-preassignment.herokuapp.com/)
* More about the assignment [here](https://www.reaktor.com/junior-dev-assignment/)