import React from 'react'
import ReactDOM from 'react-dom'

const AuditSearch = () =>
    <div>
        <h1>React Lives</h1>
    </div>


ReactDOM.render(
    React.createElement(AuditSearch, window.props),
    window.react_mount,
)