import { Button } from '@mui/material';
import React from 'react';
import { Link } from 'react-router-dom';
import { CenterSpace } from './components/Navbar/NavbarElements';

export const ShowProjects =({pros,name,onDelete})=>{
    
const handleDelete = (pro) => {
    console.log(pro.proid)
    onDelete(pro.user,pro.proid)
}

    return (
    <div >
      <CenterSpace>
      <table>
      <tbody>
        <tr>
            <th>Project name</th>
            <th>Description</th>
            <th>ProjectID</th>
            <th>Date created</th>
            <th>Action</th>
        </tr>
        {(typeof pros==='undefined')?(
                <p >Loading...</p>):(
                    pros.map((pro,i) => (
                        <tr className="project_line" key={i}>
                            <td>{pro.proname}</td>
                            <td>{pro.prodesc}</td>
                            <td>{pro.proid}</td>
                            <td>{pro.prodate}</td>
                            <td>
                                <Button onClick={()=>handleDelete(pro)}>Delete</Button>
                                <Link to={"/project/"+pro.user+"/"+pro.proid}>Enter</Link>
                            </td>
                        </tr>
                    ))
            )}
      </tbody>
      </table>
      </CenterSpace>
    </div>
    )
}