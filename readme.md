# Create your site

After you've installed Zensical, you can bootstrap your project
documentation using the `zensical` executable. Go to the directory where you want
your project to be located and enter:

[installed]: get-started.md

```
zensical new .
```

This creates the following structure:

``` .sh
.
├─ .github/
├─ docs/
│  ├─ index.md
│  └─ markdown.md
└─ zensical.toml
```

To learn more about the specific files and directories that are generated for
you, please consult the usage guide for the [`new` command][new].

[new]: usage/new.md#usage

## Configuration

Zensical comes with many [configuration options] that have sensible defaults,
which allows to build a documentation site with almost no configuration.
[`site_name`][site_name] is the only required setting:[^1]

  [^1]:
    [`site_name`][site_name] is currently required because MkDocs, the static
    site generator Zensical replaces, requires it. We plan to make this setting
    optional in a future release.

[site_name]: setup/basics.md#site_name
[site_url]: setup/basics.md#site_url

``` toml
[project]
site_name = "My site"
```

Unless you're building documentation for [offline usage], it's strongly
recommended to specify the [`site_url`][site_url] setting as well, since it's a
prerequisite for the following features:

- [Instant navigation]
- [Instant previews]
- [Custom error pages]

[configuration options]: setup/basics.md
[offline usage]: setup/offline.md
[Custom error pages]: customization.md#custom-error-pages
[Instant navigation]: setup/navigation.md#instant-navigation
[Instant previews]: setup/navigation.md#instant-previews
[setup]: setup/index.md

## Preview as you write

Zensical includes a web server, so you can preview your documentation site as
you write. The server will automatically rebuild the site when you make changes
to source files. Start it with:

``` sh
zensical serve
```

Point your browser to [localhost:8000][live preview] and you should see:

[![Creating your site]][Creating your site]
[![Creating your site dark]][Creating your site dark]

  [live preview]: http://localhost:8000
  [Creating your site]: assets/screenshots/creating-your-site.png#gh-light-mode-only
  [Creating your site dark]: assets/screenshots/creating-your-site-dark.png#gh-dark-mode-only

## Build your site

When you're finished editing, you can build a static site from your Markdown
files with:

```
zensical build
```

## Custom Scripts
# Navigation Generator
The scripts/generate_nav.py script automatically generates the navigation structure based on the docs/ folder hierarchy:

Reads directory structure and .order files for custom ordering
Extracts page titles from frontmatter when available, falls back to filename
Automatically formats category names (e.g., eat_and_drink becomes Eat & Drink)
Updates the nav section in zensical.toml after the copyright field
Handles both single-line and multi-line copyright declarations
The script ensures the navigation stays synchronized with the documentation structure without manual updates.

### Responsive Images Generator
The scripts/generate_responsive_images.py script processes images to create responsive versions:

Optimizes images for web delivery
Generates multiple sizes for responsive design
Integrates with the Zensical build process
GitHub Actions Workflow
The site uses a comprehensive CI/CD pipeline configured in .github/workflows/documentation.yml:

### Build Job:

Checks out code and sets up Python
Installs Zensical and BeautifulSoup4
Runs the responsive images script
Executes the navigation generator
Builds the site with zensical build --clean
Uploads the built site as an artifact
### Deploy Job:

Deploys the built site to GitHub Pages when the build succeeds
Configures the deployment environment

### Fallback Deploy:

Provides a safety mechanism to deploy a previous successful build if the current build fails
Ensures site availability even when new changes introduce build issues
