import React, {useState, useEffect,useRef} from 'react';
import 'react-toastify/dist/ReactToastify.css';
import Questionnaire from '../Question/Question';
import Pagination from '@mui/material/Pagination';

  export default function MemberScreen(props) { 
    
    const [currentComponent,setCurrentComponent] = useState(0)
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
      switch(itemToAdd["type"]) {
        case "questionnaire":

          return (<Questionnaire questionnaire = {itemToAdd} send ={sendData}/>)
          
          break;
        case "":
          break;
        default:
          console.log("SubWindow::getComponent::default block ~ ")

      } 

    }
    const handlePaginationChange = (event,value) => {
      setCurrentComponent(value)
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
