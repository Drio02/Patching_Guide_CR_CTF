# Sinatra

# Vuln 1: backticks pasan por la shell
post '/ping' do
  `ping -c 1 #{params[:host]}`             # host = "x; cat /data/flags/*"
end

# Vuln 2: system con un solo string tambien usa la shell
get '/archive' do
  system("tar czf /tmp/out.tgz notes/#{params[:dir]}")
  send_file '/tmp/out.tgz'
end

# Vuln 3: open() con "|" al inicio ejecuta un comando (Kernel#open)
get '/read' do
  open(params[:file]).read                 # file = "|id"
end
