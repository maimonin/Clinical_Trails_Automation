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



  export default function MemberScreen(props) { 
    
    const [currentComponent,setCurrentComponent] = useState(0)
    const [items,setItems] = useState([]);
    const [numOfItems,setNumOfItems] = useState (0)
    const ws = useRef(new W3CWebSocket('ws://127.0.0.1:7890'));



    useEffect(() => {
        var register=props.user;
        register.type = "register"
        ws.current.onopen = () => ws.current.send(JSON.stringify(register));
        ws.current.onclose = () => console.log("ws closed");
        ws.current.onmessage = (message) => {
          console.log("SubWindow::useEffect::ws.onmessage ~~ got item! "+JSON.stringify(message))
          addItem(JSON.parse(message.data))
        };  
        const wsCurrent = ws.current;

        return () => {
            wsCurrent.close();
        };
    }, []);

    useEffect(()=>setNumOfItems(items.length),[items])

    const addItem = (itemToAdd) => {
      if (isNotification(itemToAdd)){
          handleIncomingNotification(itemToAdd)
      }
      else{

        const incoming_component = getComponent(itemToAdd)

        setItems(prevState =>[ incoming_component,...prevState])

        if (currentComponent == 0){
          setCurrentComponent(1);
        }
      }
    }
   
    const isNotification = (item) => false

    const sendData = (object_to_send) =>{
      if (!ws.current) return;
      object_to_send.id = props.user.id
      
      ws.current.send(JSON.stringify(object_to_send))
      let newArr = [...items];
      newArr.splice(currentComponent,1)
      setItems(newArr)
    }
    
    const getComponent = (itemToAdd) => {
      // return (<TestNotification test={1}/>)
      switch(itemToAdd["type"]) {
        case "questionnaire":

          return (<Questionnaire questionnaire = {itemToAdd} send ={sendData}/>)
          
          break;
        case "":
          break;
        default:
          console.log("SubWindow::getComponent::default block ~ ")

          // code block
      } 
      // <TestQuestionnaire/>  //change to switch case, and parse json accordingly

    }
    const handlePaginationChange = (event,value) => {
      setCurrentComponent(value)
    }
    const handleIncomingNotification = (text) =>
    {
      toast(text, {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        containerId: props.id  

        });
    }
    const styles = {
      position: 'relative',
    
    };
  return (
    <div>
    <Card sx={{ maxWidth: 345 , minHeight:300, maxHeight:300 }} >
      <CardHeader
        avatar={
          <PersonIcon>
            
          </PersonIcon>
        }
        action={
          <IconButton aria-label="settings" onClick  = {handleIncomingNotification}>
            <MoreVertIcon  /> {/* change it to fynamically */}

          </IconButton>
        }
        title={props.name}
        subheader={props.role}
      />

{/* Same as */}
      <CardContent >
        <div  style={ {scrollBehavior: "smooth", overflowY: "scroll" , maxHeight:210}}>
        {currentComponent>0? items[currentComponent-1]: undefined}


      <Pagination count={numOfItems} page={currentComponent} onChange={handlePaginationChange} size="small"/>

      </div>
        <Typography variant="body2" color="text.secondary">

            {/* <Questionnaire /> */}
        </Typography>


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
  );
}
