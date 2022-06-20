import React from "react";
import { Button,Stack } from "@mui/material";


export default function TestNotification(props){



    return (<div>
        <Stack>
                
                <div>
                  <span>  Name:{props.test_notification.name} <br/>
                    Insturctions:{props.test_notification.instructions} <br/>
                    Patient:{props.test_notification.patient} <br/><br/>
                </span>
                    </div>
                
        
                    </Stack>
        
                    <Button variant="contained" onClick={props.dismiss}>Done</Button>
            </div>)
}

