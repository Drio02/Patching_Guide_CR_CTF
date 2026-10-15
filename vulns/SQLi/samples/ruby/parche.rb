# Sinatra + Sequel / ActiveRecord

# Patch 1: placeholders en Sequel
post '/login' do
  user = DB["SELECT * FROM users WHERE username = ? AND password = ?",
            params[:username].to_s, params[:password].to_s].first
  halt 401 unless user
  session[:user] = user[:username]
end

# Patch 2: forma hash / placeholder en ActiveRecord
get '/notes' do
  Note.where(owner: params[:owner].to_s).to_json
  # o: Note.where("owner = ?", params[:owner])
end

# Patch 3: allowlist para order
SORTABLE = %w[title created_at].freeze
get '/list' do
  col = SORTABLE.include?(params[:sort]) ? params[:sort] : 'created_at'
  Note.order(col).to_json
end
