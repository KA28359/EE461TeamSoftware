import { NavLink as Link } from 'react-router-dom';
import styled from 'styled-components';

//nav bar itself
export const Nav = styled.nav`
  background: #CC5500;
  height: 85px;
  display: flex;
  justify-content: space-around;
  //padding: 0.2rem calc((100vw - 1000px) / 2);
  z-index: 12;
  /* Third Nav */
  /* justify-content: flex-start; */
`;
  
//words in nav bar (TEAM SOFTWARE)
export const NavLink = styled(Link)`
color: #ffffff;
display: flex;
font-size: 2.5em;
align-items: center;
text-decoration: none;
padding: 0 1rem;
height: 100%;
cursor: pointer;

`;

// used to center items
export const CenterForm = styled.div`
display: flex;
justify-content: center;
`;

export const CenterSpace = styled.div`
display: flex;
justify-content: center;
margin-top: 30px;
`;
  
//menu that contains all of the options in the nav bar
export const NavMenu = styled.div`
  display: flex;
  align-items: center;
  margin-right: -24px;
  /* Second Nav */
  /* margin-right: 24px; */
  /* Third Nav */
  /* width: 100vw;
  white-space: nowrap; */
  @media screen and (max-width: 768px) {
    display: none;
  }
`;
  
//button in the nav bar
export const NavButton = styled.button`
  
  margin-right: 24px;
  border-radius: 4px;
  background: #ffffff;
  color: #000000;
  padding: 10px 22px;
  outline: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-decoration: none;
  @media screen and (max-width: 768px) {
    display: none;
  }
`;

//login buttons
export const LogBtn = styled.button`
border-radius: 4px;
background: #CC5500;
color: #ffffff;
padding: 10px 22px;
outline: none;
border: none;
cursor: pointer;
transition: all 0.2s ease-in-out;
text-decoration: none;

`;
  
