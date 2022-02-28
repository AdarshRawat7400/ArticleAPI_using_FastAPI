
api_details = {
"title" : 'Article API'
,
'description' : '''
This is the API for the article.
users can create, read, update and delete articles.
'''
,
'version' : '0.1.0'

}
tags_metadata = [

    {
        "name": "Authentication",
        "description": '''
        This Authentication endpoint provide jwt (lifetime of 30 min) token after verify user credentials:''',
        
    },
    {
        "name": "Users",
        "description": '''
        Users can create, read users. with the following endpoints:'''
    },
      
    {
        "name": "Articles",
        "description": '''
        Articles can create, read, update and delete articles. with the following endpoints:''',
        
    },
]