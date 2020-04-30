@Echo OFF
 
SET save=
SET /p save=COMMENTAIRE SAUVEGARDE:
git add .
git commit -m %save%
git push origin master
echo 
echo sauvegarde effectuee correctement 
pause