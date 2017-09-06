import React from 'react'
import ReactDOM from 'react-dom'
import AuditSearch from './audit_search.react'

ReactDOM.render(
    React.createElement(AuditSearch, window.props),
    window.react_mount,
)