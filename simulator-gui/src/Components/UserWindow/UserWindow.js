import React, {useState, useEffect,useRef} from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import PersonIcon from '@mui/icons-material/Person';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import MoreVertIcon from '@mui/icons-material/MoreVert';
import Questionnaire from '../Question/Question';

import Pagination from '@mui/material/Pagination';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import MemberScreen from '../MemberScreen/MemberScreen';
import RegisterScreen from '../RegisterScreen/RegisterScreen';
import { getComponent, isComponent } from '../../Utils/ComponentsManger';
export const blankUser = {"name": "", "role": "",
"sex": "", "age": -1,"id": -1};

export default function UserWindow(props) { 
    const webSocket = useRef(null)
    const [userDetails,setUserDetails] = useState(blankUser)
    const [items,setItems] = useState([]);

 
    useEffect(() => {
        webSocket.current = new W3CWebSocket('ws://127.0.0.1:7890');
        webSocket.current.onopen = () => console.log("ws opened");
        webSocket.current.onclose = () => console.log("ws closed");
        webSocket.current.onmessage = (message)=>addItem(JSON.parse(message.data))

    }, []);
    const debug =(message) => {
      console.log(message)
      console.log(JSON.parse(message.data))
    }
    const sendRegister  = (userDetails) =>
    {
      var register_request = {...userDetails}
      register_request["type"] = "register"
      register_request["workflow"] = props.workflow_id  
      webSocket.current.send(JSON.stringify(register_request))
      setUserDetails(userDetails)
    }
    const styles = {
        position: 'relative',
      
      };
    const sendData = (object_to_send,component_index_to_delete) =>{
        object_to_send.id = userDetails.id   
        object_to_send.workflow_id = props.workflow_id     
        webSocket.current.send(JSON.stringify(object_to_send))
        let newArr = [...props.items];
        newArr.splice(component_index_to_delete,1)
        setItems(newArr)
      }
      const isNotification = (item) => false

    const addItem = (itemToAdd) => {
      console.log("UserWindow::addItem ~ " + JSON.stringify(itemToAdd))
      if (isNotification(itemToAdd)){
          //handleIncomingNotification(itemToAdd)
      }
      else{
        if(isComponent(itemToAdd)){
          const incoming_component = getComponent(itemToAdd)
          setItems(prevState =>[incoming_component,...prevState])
        }
        }
      }
    
return (
    <div>
    <Card sx={{ maxWidth: 345 , minHeight:300, maxHeight:300 }} >
      <CardHeader
        avatar={ // TODO: Change according to userDetails.role
          <PersonIcon>
            
          </PersonIcon>
        }
        action={
          <IconButton aria-label="settings" >
            <MoreVertIcon  /> {/* change it to dynamically */}

          </IconButton>
        }
        title={props.name}
        subheader={props.role}
      />

{/* Same as */}
      <CardContent >
        <div  style={ {scrollBehavior: "smooth", overflowY: "scroll" , maxHeight:210}}>

        {userDetails == blankUser? <RegisterScreen sendRegister={sendRegister}/> 
                                 : <MemberScreen webSocket={webSocket.current} user={userDetails} items={items} sendData={sendData} />}
       
      </div>



      </CardContent>
      <ToastContainer style={styles}
  position="top-right"
  autoClose={5000}
  hideProgressBar={false}
  newestOnTop={false}
  closeOnClick
  rtl={false}
  pauseOnFocusLoss
  draggable
  pauseOnHover
  containerId={props.id}
  enableMultiContainer
  limit ={1}
/>

    </Card>
    </div>
)
}
