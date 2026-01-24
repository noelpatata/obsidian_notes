	``` bash
	git init
	git add .
	git commit -m "a"
	git checkout -b noel
	git remote add origin git@github.com:noelpatata/NFCheckin_Backend.git
	git pull --rebase origin noel
	git push -u origin noel
	```