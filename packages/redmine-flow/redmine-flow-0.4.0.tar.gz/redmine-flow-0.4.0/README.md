h1. Project Organization Tools - the handbook


h2. Motivation

We have a diversity of software tools for different aspects of project organization, complicated by some diversity of associated projects (e.g. CDCI, INTEGRAL, and some scientific projects are co-developed and interlinked) and organizations.

In all cases it is necessary to ensure that documents are findable, accessible, and interoperable.
This is ensured by maintaining *bidirectional references with suitable metadata for all developments and activities*.

h2. Available platforms

* https://redmine.astro.unige.ch/

the best available solution for issue management in the Department seems to be the redmine. It also supports

* https://gitlab.astro.unige.ch/

code-heavy projects yield inevitably actions in code projects, such as Merge Requests (Pull Requests) and possibly issues. 

* https://gitlab.unige.ch/

there is also an institutional solution, which has andvantage of authenticating many Swiss institutions, as well as any user with free SWITCHedu account.

* https://gitlab.in2p3.fr/

for projects with strong French contribution, we use highly advanced platform of CNRS/IN2P3.

* https://github.com/

for projects with wide public reach, it is suitable to use a world-wide platform, with high potential for code discoverability and cross-institute collaboration

_examples_: https://github.com/volodymyrss/pygcn

* https://overleaf.com/

an ideal and widely used solution for collaborative edititing

* google docs

* office365


* ESA's SOCCI (confluece, etc)

handles document management, issue tracking, workflows, for ESA projects. Considered the reference for ESA collaboration.

_example_ :https://issues.cosmos.esa.int/socciwiki/display/INT/ISDC-EXPRO-TN-0005

* taskwarrior, or other personal management tools

a tool for private management, as no shared task server is available (or should be available). 

h2. Activity aspects

h3. Document management

redmine.astro.unige.ch wiki

overleaf

h3. Code management

gitlab and github instances are associated with code management.

*recommendation*: for every project, insert a reference in an upstream document, and add metadata

h3. Issue tracking

Essentially all of the issue tracking systems have suitable API's, which can be integrated, for example, with bugwarrior. The upstream issue management is considered to be *redmine*, meaning that only those issues that end up in redmine are ensured to be followed up. 

Collaborators are not, however, restricted from making private TODO lists, possibly managed by taskwarrior. 
