window.MathJax = {
  loader: { load: ['[tex]/ams'] },
  tex: {
    packages: { '[+]': ['ams'] },
    inlineMath: [['$', '$'], ['\$', '\$']],
    tags: 'all',
    tagSide: 'right',
    tagIndent: '0.8em'
  },
  options: {
    renderActions: {
      addMenu: [0, '', ''],
      addCopyText: [0, '', '']
    }
  },
  startup: {
    typeset: false
  }
};