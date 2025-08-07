const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api/elasticsearch',
    createProxyMiddleware({
      target: process.env.REACT_APP_ELASTICSEARCH_HOST || 'http://elasticsearch:9200',
      changeOrigin: true,
      pathRewrite: {
        '^/api/elasticsearch': ''
      },
      headers: {
        'x-elastic-client-meta': 'react-search-ui'
      },
      onError: (err, req, res) => {
        res.status(500).json({
          error: 'Elasticsearch connection failed',
          details: err.message
        });
      }
    })
  );
};