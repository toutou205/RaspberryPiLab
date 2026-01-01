$User = "alex"
$HostIP = "192.168.3.13"
$BaseRemotePath = "/home/alex/ProjectVenv/MCP_Sever_Practice"
$TargetFolder = "PiSmartDisplay"
$LocalPath = "d:\work\MCP_Severs\project_root_mcp_old"

Write-Host "Deploying to $User@${HostIP}:${BaseRemotePath}/${TargetFolder} ..."

# 1. Setup Remote Directory (Clean Slate)
Write-Host "Cleaning up previous deployment..."
# Remove the entire BaseRemotePath to ensure we clean up the loose files from before
# Then recreate it
ssh $User@$HostIP "rm -rf ${BaseRemotePath} && mkdir -p ${BaseRemotePath}"

# 2. Copy Files as a specific folder
Write-Host "Copying project folder..."
# scp -r local_dir remote:dest_path/new_dir_name
# Note: scp -r source dest: if dest does not exist, it creates it as a copy of source.
scp -r "$LocalPath" "$User@${HostIP}:${BaseRemotePath}/${TargetFolder}"

Write-Host "---------------------------------------------------"
Write-Host "Deployment Complete!"
Write-Host "Files are located at: ${BaseRemotePath}/${TargetFolder}"
Write-Host "Virtual Environment: /home/alex/ProjectVenv/bin/python"
Write-Host "See mcp_server_config.json for the updated client configuration."
Write-Host "---------------------------------------------------"
