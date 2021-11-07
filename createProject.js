import React, { Component } from 'react';
import {
  LogBtn,
  CenterForm,
} from './Navbar/NavbarElements';
import TextField from '@mui/material/TextField';

export const CreateProject =({onSubmit,setName,setDesc,setId})=>{

    const handleSubmit = (event) => {
        onSubmit()
}

    return(
        <div>
        <CenterForm>
          <TextField onChange = {(event) => setName(event.target.value)} id="outlined-basic" label="Project name" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
          <TextField onChange = {(event) => setDesc(event.target.value)} id="outlined-basic" label="Description" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
          <TextField onChange = {(event) => setId(event.target.value)} id="outlined-basic" label="ProjectID" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
          <LogBtn onClick={handleSubmit} type = "submit">Create project</LogBtn>
        </CenterForm>
        </div>
    );
}