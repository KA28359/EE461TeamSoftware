import React, { useRef }  from 'react';
import {
  LogBtn,
  CenterForm,
} from './components/Navbar/NavbarElements';
import TextField from '@mui/material/TextField';

export const CreateProject =({onSubmit,setName,setDesc,setId})=>{
  let textInputOne = useRef(null);
  let textInputTwo = useRef(null);
  let textInputThree = useRef(null);
    const handleSubmit = (event) => {
      textInputOne.current.value = "";
      textInputTwo.current.value = "";
      textInputThree.current.value = "";
        onSubmit()
}

    return(
        <div>
        <CenterForm>
          <TextField inputRef={textInputOne} onChange = {(event) => setName(event.target.value)} id="outlined-basic" label="Project name" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
          <TextField inputRef={textInputTwo} onChange = {(event) => setDesc(event.target.value)} id="outlined-basic" label="Description" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
          <TextField inputRef={textInputThree} onChange = {(event) => setId(event.target.value)} id="outlined-basic" label="ProjectID" variant="outlined" margin="normal" />
        </CenterForm>
        <CenterForm>
          <LogBtn onClick={handleSubmit} type = "submit">Create project</LogBtn>
        </CenterForm>
        </div>
    );
}