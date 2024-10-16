import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "Music Dashboard Docs",
  tagline: "A spotify integrated music library dashboard.",
  favicon: "/img/favicon.ico",

  // Set the production url of your site here
  url: "https://dashspot-dev.netlify.app",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",

  // GitHub pages deployment config.
  projectName: "spotify-dashboard", // Repo name

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          routeBasePath: "/",
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: "img/docusaurus-social-card.jpg",
    colorMode: {
      defaultMode: "dark",
      disableSwitch: true,
    },
    navbar: {
      title: "Music Dashboard",
      logo: {
        alt: "App Icon",
        src: "img/logo.png",
      },
      items: [
        {
          type: "docSidebar",
          sidebarId: "docsSidebar",
          position: "left",
          label: "Docs",
        },
        {
          href: "https://github.com/desertthunder/spotify-dashboard",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Social Links",
          items: [
            {
              label: "GitHub",
              href: "https://github.com/desertthunder",
            },
            {
              label: "LinkedIn",
              href: "https://www.linkedin.com/in/owais-jamil/",
            },
            {
              label: "Twitter",
              href: "https://twitter.com/_desertthunder",
            },
          ],
        },
        {
          title: "Resources",
          items: [
            {
              label: "React",
              href: "https://react.dev",
            },
            {
              label: "Docusaurus",
              href: "https://docusaurus.io",
            },
            {
              label: "Spotify API Documentation",
              href: "https://developer.spotify.com/documentation/web-api/",
            },
          ],
        },
        {
          title: "More",
          items: [
            {
              label: "My Blog",
              href: "https://desertthunder.github.io",
            },
            {
              label: "Digital Garden",
              href: "https://desertthunder.github.io/garden",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Owais J. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
