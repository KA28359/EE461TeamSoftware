import React, { Component,useState,useEffect } from 'react';
import {CenterForm,CenterSpace } from '../Navbar/NavbarElements';
import './resource.css'

export default function HwTable ({name, proid}){
    const [info, setInfo]=useState([{}])
    const [history, setHistory]=useState([{}])
    const [error,setError] = useState('');
    const [out, setOut]=useState('')
    const [checkin, setCheckin]=useState('')
    const [adduser,setAdduser]=useState('')

    useEffect(()=>{
        fetch("http://127.0.0.1:5000/api/project/hardware",
            {method:'post',credentials: 'include', headers:{"Content-Type": "application/json"},
            body:JSON.stringify({'name':name.toString(), "proid":proid.toString()})})
          .then(response => response.json())
          .then(data => {
              setInfo(data.info)
              setHistory(data.history)
              console.log(data)})
        },[])
    const updateData=()=>{
        fetch("http://127.0.0.1:5000/api/project/hardware",
            {method:'post',credentials: 'include', headers:{"Content-Type": "application/json"},
            body:JSON.stringify({'name':name.toString(), "proid":proid.toString()})})
          .then(response => response.json())
          .then(data => {
              setInfo(data.info)
              setHistory(data.history)
              console.log(data)})
    }
    
    const handleCheckout = (value) =>{
        setOut(value)
    }
    const handleCheckin = (value) =>{
        setCheckin(value)
    }
    const handleAdduser = (value) =>{
        setAdduser(value)
    }

      const handleSubmit=(hwname)=>{
        fetch('http://127.0.0.1:5000/api/project/hardware/checkout',{
        method:"POST",
        body:JSON.stringify({
            'name':name.toString(), 
            "proid":proid.toString(),
            "checkout":out,
            "hwname":hwname
        }),
        headers:{
            "Content-type":"application/json; charset=UTF-8",
            "Access-Control-Allow-Headers":"Content-Type",
            "Access-Control-Allow-Credentials":"true"
        }
    }).then(res => res.json())
    .then(data => {
            updateData()
            setOut('')
            if (data.error != ""){
                setError(data.error)}
    })
    }
    const submitCheckin=(hwname,hwid)=>{
        fetch('http://127.0.0.1:5000/api/project/hardware/checkin',{
        method:"POST",
        body:JSON.stringify({
            'name':name.toString(), 
            "proid":proid.toString(),
            "checkin":checkin,
            "hwname":hwname,
            "historyid":hwid
        }),
        headers:{
            "Content-type":"application/json; charset=UTF-8",
            "Access-Control-Allow-Headers":"Content-Type",
            "Access-Control-Allow-Credentials":"true"
        }
    }).then(res => res.json())
    .then(data => {
            updateData()
            setCheckin('')
            if (data.error != ""){
                setError(data.error)}
    })
    }

    const submitAdd=()=>{
        fetch('http://127.0.0.1:5000/api/project/hardware/adduser',{
        method:"POST",
        body:JSON.stringify({
            'name':name.toString(), 
            "proid":proid.toString(),
            "usertoadd":adduser
        }),
        headers:{
            "Content-type":"application/json; charset=UTF-8",
            "Access-Control-Allow-Headers":"Content-Type",
            "Access-Control-Allow-Credentials":"true"
        }
    }).then(res => res.json())
    .then(data => {
            updateData()
            setAdduser('')
            if (data.error != ""){
                setError(data.error)}
    })
    }


     return(
        <div>
          <div>
              <p>Current Project: ID({proid})</p>
          </div>
          <CenterSpace>
            <div>
                <p>Add another user to this project:</p>
                    <form onSubmit={()=>submitAdd}>
                            <input type="text" id="add-user" lable="username" onChange={(event) => handleAdduser(event.target.value)} />
                            <input type="submit" value="add user" />
                    </form>
            </div>
          </CenterSpace>
            <CenterSpace>
            <p className="tabletitle">Hardware Information:</p>
            </CenterSpace>
            <CenterSpace>
            <div className="info_table">
                  <table>
                  <tbody>
                      <tr>
                        <th>Hardware</th>
                        <th>Capacity</th>
                        <th>Available</th>
                        <th>Request</th>
                     </tr>
                     {(typeof info==='undefined')?(
                        <p >Loading...</p>):(
                        info.map((hw,i) => (
                     <tr className="hardwares_line" key={i}>
                            <td>{hw.hwname}</td>
                            <td>{hw.capacity}</td>
                            <td>{hw.avail}</td>
                            <td>
                                <div>
                                <form onSubmit={()=>handleSubmit(hw.hwname)} >
                                    <input type="text" onChange={(event) => handleCheckout(event.target.value)} className="checkoutbox"></input><br/>
                                    <input type="submit" className="submit" value="checkout"></input>
                                </form>
                                </div>
                            </td>       
                     </tr>
                     ))
                  )}
                  </tbody>
                  </table>
          </div>
          </CenterSpace>
          <CenterSpace>
            <p className="tabletitle">Your checking history:</p>
            </CenterSpace>
            <CenterSpace>
            <div className="history_table">
                  <table>
                  <tbody>
                      <tr>
                        <th>Hardware</th>
                        <th>Checkout amount</th>
                        <th>Checkout date</th>
                        <th>Remain</th>
                        <th></th>
                     </tr>
                     {(typeof history==='undefined')?(
                        <p >Loading...</p>):(
                        history.map((his,i) => (
                     <tr className="histories_line" key={i}>
                            <td>{his.hwname}</td>
                            <td>{his.amount}</td>
                            <td>{his.date}</td>
                            <td>{his.remain}</td>
                            <td>
                                <div>
                                <form onSubmit={()=>submitCheckin(his.hwname,his.id)} >
                                    <input type="text" onChange={(event) => handleCheckin(event.target.value)} className="checkinbox"></input><br/>
                                    <input type="submit" className="submit" value="checkin"></input>
                                </form>
                                </div>
                            </td>       
                     </tr>
                     ))
                  )}
                  </tbody>
                  </table>      
          </div>
          </CenterSpace>
          <CenterForm>
              {error?<p style={{ color: 'red' }}>{error}</p>:<p> </p>}
          </CenterForm>
        </div>
      )
}