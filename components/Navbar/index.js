
import React from 'react';
import {Link} from 'react-router-dom';
import {
  Nav,
  NavLink,
  NavMenu,
  NavButton
} from './NavbarElements';

//creating the Navbar at the top of the screen
  
const Navbar = () => {
  return (
    <>
      <Nav> {/* styled component which is basically just the orange bar in the background */}
  
        <NavMenu> 
        {/* The NavLink is like a button, once pressed it sends us to the given path */}
        <NavLink to='/'>TEAM SOFTWARE</NavLink>
        </NavMenu>
        <NavMenu>
        {/* Link to go to when button pressed */}
        <Link to='/signin' >
        {/* NavButton are the two buttons on the top */}
        <NavButton >Sign In</NavButton>
        </Link>
        <Link to='/signup' >
        <NavButton>Sign Up</NavButton>
        </Link>
        </NavMenu>
      </Nav>
    </>
  );
};
  
export default Navbar;