# Motivation
Our application only requires a subset of plot types, so we create a [partial bundle](https://github.com/plotly/plotly.js/blob/master/dist/README.md#partial-bundles) for reduced bundle sizes.

# Bundling [plotly.js](https://github.com/plotly/plotly.js) with Webpack

Usage (works with NPM or Yarn):

```bash
npm install
npm run webpack-dev   #takes ~5s for a 2.8MB bundle
npm run webpack-prod  #takes ~7s for a 0.9MB bundle
```

The `index.js` file included in this folder loads all of plotly.js.
