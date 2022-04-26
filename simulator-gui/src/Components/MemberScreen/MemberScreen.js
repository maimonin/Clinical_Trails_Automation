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



  export default function MemberScreen(props) { 
    
    const [currentComponent,setCurrentComponent] = useState(0)
    const [items,setItems] = useState([]);
    const [numOfItems,setNumOfItems] = useState (0)


    useEffect(()=>{
      setNumOfItems(props.items.length)
      if(currentComponent >= props.items.length){
          props.items.length==0? setCurrentComponent(0) : setCurrentComponent(1)
        }
      if( props.items.length>0 & currentComponent ==0){
        setCurrentComponent(1)
      }
    },[props.items])

    

    const sendData = (object_to_send) =>props.sendData(object_to_send,currentComponent);
     
    
    
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
         {currentComponent>0? props.items[currentComponent-1]: undefined}


      <Pagination count={numOfItems} page={currentComponent} onChange={handlePaginationChange} size="small"/>

    </div>
  );
}
