import React, { useState,useEffect } from 'react';
import {CenterSpace } from './components/Navbar/NavbarElements';
import './resource.css'
import moment from "moment-timezone"
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
            setError(data.error)
            setOut('')
            updateData()          
    })
    document.getElementById(hwname).value = "";
    
    }
    const submitCheckin=(hwname,hwid,remain)=>{
        if(remain<checkin){
            setError("wrong number: please check your input")
        }
        else{
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
                setCheckin('')
                setError(data.error)
                updateData()
        })
        }
        document.getElementById(hwid).value = "";

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
        }).then(res => res.json()).then(data => {
            setAdduser('')
            setError(data.error)
            updateData()
    })
    document.getElementById("add-user").value = "";
    }

    const handleDelHis=(remain,id)=>{
        if (remain !== 0){
            setError('Cannot delete: check-in required')
        }
        else{
            fetch('http://127.0.0.1:5000/api/project/hardware/history_delete',{
            method:"POST",
            body:JSON.stringify({
                'name':name.toString(), 
                "proid":proid.toString(),
                "historyid":id
            }),
            headers:{
                "Content-type":"application/json; charset=UTF-8",
                "Access-Control-Allow-Headers":"Content-Type",
                "Access-Control-Allow-Credentials":"true"
            }
            }).then(res => res.json())
            .then(data => {
                if(data.error==="None"){
                    updateData()
                    setError('')
                }
                else if (data.error !== ''){
                    setError(data.error)}
    })
    }
}


     return(
        <div>
          <div>
              <h1 style={{textAlign:"center"}}>Current Project: ID({proid})</h1>
              <p style={{ color: 'red', textAlign:"center" }}>{error}</p>
          </div>
          <CenterSpace>
            <div>
                <p>Add another user to this project:</p>
                <form>
                            <input type="text" id="add-user" lable="username" onChange={(event) => handleAdduser(event.target.value)} />
                    </form>
                    <button type="submit" className="submit" onClick={(event)=>submitAdd()}>add user</button>
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
                                <form  >
                                    <input id={hw.hwname} type="text" onChange={(event) => handleCheckout(event.target.value)} className="checkoutbox"></input><br/>
                                </form>
                                <button type="submit" className="submit" onClick={(event)=>handleSubmit(hw.hwname)}>checkout</button>
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
                            {/* <td>{his.date}</td> */}
                            <td>{moment(his.date).format('DD/MM/YYYY HH:mm')}</td>
                            <td>{his.remain}</td>
                            <td>
                                <div>
                                <form >
                                    <input id={his.id} type="text" onChange={(event) => handleCheckin(event.target.value)} className="checkinbox"/><br/>
                                </form>
                                <button type="submit" className="submit" onClick={(event)=>submitCheckin(his.hwname,his.id,his.remain)}>checkin</button>
                                <button className="submitdel" onClick={(event)=>handleDelHis(his.remain,his.id)}>delete</button>
                                </div>
                            </td>       
                     </tr>
                     ))
                  )}
                  </tbody>
                  </table>      
          </div>
          </CenterSpace>
        </div>
      )
}