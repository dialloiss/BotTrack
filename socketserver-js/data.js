import {parse} from "urlparser"

let dataModel ={    
    Title:{
        company_id:"",
        activity_id:"",
        employee_id:"",
        activity_starttimestamp:"",
        activity_endtimestamp:"",
        title_recognition_id:"",
        duration:"",
        activity_idl_time:"",
    },

    Activity :{
        company_id:"",
        employee_id:"",
        computer_id:"",
        category_id:"",
        activity_recognition_id:"",
        activity_exe:"",
        activity_class:"",
        activity_classified_by:"",
    },

    titleRecognition : {  
        title_name:"",
    },

    activityRecognation :{
        activity_type:"",
        activity_name:"",
        activity_description:"",
        activity_category:"",
    }
};


function dataModeler(arg){
    let data = dataModel;
    data.Title.activity_starttimestamp=arg[0];
    data.Title.company_id=arg[12]
    data.Title.activity_endtimestamp=arg[1];
    data.Title.duration=arg[5];
    data.Title.activity_idl_time=arg[8];
    data.Title.employee_id=arg[13];
    data.Activity.employee_id=arg[13];
    data.Activity.company_id=arg[12];
    data.Activity.activity_exe=arg[2];
    data.titleRecognition.title_name=arg[3];
    if(arg[10]==""){
        data.activityRecognation.activity_type="Application"
        data.activityRecognation.activity_name=arg[2]
        data.Activity.activity_class="Application";
    }
    else{
        const url = parse(arg[10])
        data.Activity.activity_class=url.host.hostname; 
        data.activityRecognation.activity_type=url.host.hostname;
        data.activityRecognation.activity_name=url.host.hostname
    }
}



