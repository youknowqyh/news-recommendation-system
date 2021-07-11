import React from 'react';
import Auth from '../Auth/Auth';
import PropTypes from 'prop-types';

// import './Base.css';
import { Link, withRouter } from 'react-router-dom';

const Base = function ({ children, history }) {
    return (
        <div>
            <nav className="nav-bar  light-blue darken-4">
                <div className="nav-wrapper">
                    {/* <a href="/" className="brand-logo">&nbsp;&nbsp;News Feed</a> */}
                    <Link to="/" className="brand-logo">&nbsp;&nbsp;News Feed</Link>

                    <ul id="nav-mobile" className="right">
                        {Auth.isUserAuthenticated() ?
                            (<div>
                                <li>{Auth.getEmail()}</li>
                                <li>

                                    <a href='/' onClick={() => {
                                        Auth.deauthenticateUser(() => this.props.history.push("/logout"));
                                    }}>Log out</a>
                                </li>

                            </div>)
                            :
                            (<div>
                                {/* <li><a href="/login">Log in</a></li>
                                <li><a href="/signup">Sign up</a></li> */}
                                <li><Link to="/login">Log in</Link></li>
                                <li><Link to="/signup">Sign up</Link></li>
                            </div>)
                        }
                    </ul>
                </div>
            </nav>
            <br />
            {children}
        </div>
    )
}
// 规定必须传入参数
Base.propTypes = {
    children: PropTypes.object.isRequired
};
// export default Base;
export default withRouter(Base);
