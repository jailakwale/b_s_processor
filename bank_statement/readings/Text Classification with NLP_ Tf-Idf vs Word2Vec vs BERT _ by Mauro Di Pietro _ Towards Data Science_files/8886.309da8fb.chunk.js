(self.webpackChunklite=self.webpackChunklite||[]).push([[8886],{54023:(e,n,t)=>{"use strict";t.d(n,{P:()=>c});var l=t(59713),r=t.n(l),o=t(83687),i=t(36823);function a(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);n&&(l=l.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,l)}return t}function s(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?a(Object(t),!0).forEach((function(n){r()(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):a(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var c=function(e){var n=(0,o.B)(),t=(0,i.I)();if("Collection"===e.__typename)return n(e);if("User"===e.__typename){var l,r,a,c=null!==(l=null===(r=e.customDomainState)||void 0===r||null===(a=r.live)||void 0===a?void 0:a.domain)&&void 0!==l?l:null;return t(s(s({},e),{},{domain:c}))}return""}},54415:(e,n,t)=>{"use strict";t.d(n,{v:()=>d,G:()=>m});var l=t(28655),r=t.n(l),o=t(71439),i=t(67294),a=t(73882),s=t(16831),c=t(98281);function u(){var e=r()(["\n  fragment PublisherAvatar_publisher on Publisher {\n    __typename\n    ... on Collection {\n      id\n      ...CollectionAvatar_collection\n    }\n    ... on User {\n      id\n      ...UserAvatar_user\n    }\n  }\n  ","\n  ","\n"]);return u=function(){return e},e}var d=(0,o.Ps)(u(),a.d,s.W),m=function(e){var n=e.link,t=void 0!==n&&n,l=e.scale,r=void 0===l?"M":l,o=e.publisher;switch(o.__typename){case"User":return i.createElement(c.Yt,{link:t,scale:r,user:o});case"Collection":return i.createElement(a.v,{link:t,size:c.wC[r],collection:o});default:return null}}},97297:(e,n,t)=>{"use strict";t.d(n,{gp:()=>p,DX:()=>b,b5:()=>f});var l=t(28655),r=t.n(l),o=t(71439),i=t(67294),a=t(53976),s=t(82318),c=t(98024),u=t(27390),d=t(27952);function m(){var e=r()(["\n  fragment PublisherFollowingCount_publisher on Publisher {\n    __typename\n    id\n    ... on User {\n      socialStats {\n        followingCount\n        collectionFollowingCount\n      }\n      followedCollections\n      username\n    }\n  }\n"]);return m=function(){return e},e}var p=function(e){var n,t,l,r,o=(0,a.VB)({name:"enable_fix_follow_counts",placeholder:!1}),i=null!==(n="Collection"===e.__typename?0:(null===(t=e.socialStats)||void 0===t?void 0:t.followingCount)+e.followedCollections)&&void 0!==n?n:0;return o&&"User"===e.__typename&&(i=(null===(l=e.socialStats)||void 0===l?void 0:l.followingCount)+(null===(r=e.socialStats)||void 0===r?void 0:r.collectionFollowingCount)),{followingCount:i,isFollowingCountVisible:i>0}},b=function(e){var n,t=e.publisher,l=e.linkStyle,r=void 0===l?"SUBTLE":l,o=p(t),a=o.followingCount,m=o.isFollowingCountVisible,b="User"===t.__typename?(0,d.MzF)(null!==(n=t.username)&&void 0!==n?n:""):"",f=!!b;if(!m)return null;var v="".concat((0,u.pY)(a)," Following");return f?i.createElement(s.r,{linkStyle:r,href:b},v):i.createElement(c.F,{tag:"span",scale:"L",color:"DARKER"},v)},f=(0,o.Ps)(m())},78886:(e,n,t)=>{"use strict";t.d(n,{KL:()=>V,rF:()=>z,Lk:()=>H,eB:()=>M,qy:()=>W,FB:()=>Y});var l=t(28655),r=t.n(l),o=t(59713),i=t.n(o),a=t(63038),s=t.n(a),c=t(46829),u=t(71439),d=t(67294),m=t(54023),p=t(54415),b=t(97297),f=t(44935),v=t(76532),g=t(68421),y=t(41832),E=t(42933),w=t(82318),h=t(52862),S=t(80362),_=t(98024),O=t(18579),I=t(95760),P=t(51512),C=t(6688),B=t(19551),x=t(14391),F=t(67297),L=t(27390),D=t(27952),T=t(61598);function j(){var e=r()(["\n  query PublisherSidebarFollowsQuery($userId: ID!, $limit: Int) {\n    userFollows(userId: $userId, limit: $limit) {\n      ... on User {\n        hasDomain\n        ...UserMentionTooltip_user\n        ...PublisherSidebarFollows_followedEntity\n      }\n      ... on Collection {\n        ...CollectionTooltip_collection\n        ...PublisherSidebarFollows_followedEntity\n      }\n    }\n  }\n  ","\n  ","\n  ","\n"]);return j=function(){return e},e}function k(){var e=r()(["\n  fragment PublisherSidebarFollows_followedEntity on Publisher {\n    __typename\n    id\n    name\n    ...PublisherAvatar_publisher\n  }\n  ","\n"]);return k=function(){return e},e}function U(){var e=r()(["\n  fragment PublisherSidebarFollows_user on User {\n    id\n    name\n    username\n    ...PublisherFollowingCount_publisher\n    ...userUrl_user\n  }\n  ","\n  ","\n"]);return U=function(){return e},e}function R(){var e=r()(["\n  fragment PublisherSidebarFollows_customStyleSheet on CustomStyleSheet {\n    id\n    blogroll {\n      visibility\n    }\n  }\n"]);return R=function(){return e},e}function N(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);n&&(l=l.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,l)}return t}function A(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?N(Object(t),!0).forEach((function(n){i()(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):N(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var G,$=function(e){var n=e.entity,t=e.tag,l=void 0===t?"h4":t,r=(0,C.I)()([(0,O.n)({name:"detail",scale:"S",clamp:1,leadingTrim:!1,color:"LIGHTER"}),{wordBreak:"break-all"}]),o=(0,m.P)(n);return d.createElement(E.x,{marginBottom:"8px",paddingRight:"10px",tag:"span"},d.createElement(w.r,{href:o},d.createElement(h.$,{placement:"right",targetDistance:15,mouseEnterDelay:500,mouseLeaveDelay:0,noPortal:!1,disablePortalOverlay:!0,role:"tooltip",popoverRenderFn:function(){return"User"===n.__typename?d.createElement(y.K$,{user:n}):d.createElement(f.L,{collection:n,buttonSize:"COMPACT",buttonStyleFn:function(e){return e?"OBVIOUS":"STRONG"}})}},d.createElement(l,{className:r},n.name))))},V=function(e){var n;return{isBlogrollInSidebar:(null==e||null===(n=e.blogroll)||void 0===n?void 0:n.visibility)===x.n$.BLOGROLL_VISIBILITY_SIDEBAR}},z=function(e){var n,t=null==e||null===(n=e.blogroll)||void 0===n?void 0:n.visibility,l=!t||t===x.n$.BLOGROLL_VISIBILITY_UNSET,r=t===x.n$.BLOGROLL_VISIBILITY_SIDEBAR;return{shouldShowBlogroll:!(!l&&!r||void 0===e)}},H=d.createContext({homepageUserId:null,postId:null,catalogId:null});!function(e){e[e.Initial=0]="Initial",e[e.Secondary=1]="Secondary",e[e.Dismissed=2]="Dismissed",e[e.Navigating=3]="Navigating",e[e.Updated=4]="Updated"}(G||(G={}));var M=function(e){var n,t,l=e.publisher,r=e.isVisible,o=e.customStyleSheet,i=e.withBottomBorder,a=void 0!==i&&i,u=e.withTopBorder,m=void 0===u||u,f=e.publisherTag,y=(0,C.I)(),h=(0,v.H)().value,O=(0,F.p9)((function(e){return e.config.isAmp})),T=(0,D.MzF)(null!==(n=l.username)&&void 0!==n?n:""),j=d.useState(G.Initial),k=s()(j,2),U=k[0],R=k[1],N="User"===l.__typename&&l.id===(null==h?void 0:h.id),V=(null==o||null===(t=o.blogroll)||void 0===t?void 0:t.visibility)===x.n$.BLOGROLL_VISIBILITY_HIDDEN,M=z(o).shouldShowBlogroll,W=x.T3.BLOGROLL_ENABLE,Y=M&&N&&!U&&!(null!=h&&h.dismissableFlags.includes(W)),X=(0,I.Av)(),K=d.useContext(H),Q=(0,B.g)({onPresentedFn:function(){return X.event("sidebar.blogrollViewed",A(A({},K),{},{viewerIsAuthor:N}))}}),J=(0,c.useLazyQuery)(q,{ssr:!1,variables:{userId:l.id,limit:5}}),Z=s()(J,2),ee=Z[0],ne=Z[1],te=ne.called,le=ne.loading,re=ne.error,oe=ne.data,ie=(oe=void 0===oe?{userFollows:void 0}:oe).userFollows,ae=(0,b.gp)(l).followingCount,se=d.useCallback((function(e){return function(){return d.createElement(E.x,{minWidth:"240px",padding:"16px"},d.createElement(_.F,{scale:"S",color:"WHITE"},"Blogrolls help your readers discover writers you follow. Writers who have published most recently show up at the top."),d.createElement(E.x,{marginTop:"8px"},d.createElement(_.F,{scale:"S",color:"WHITE"},Y&&d.createElement(w.r,{onClick:function(){var n,t;n=G.Dismissed,t=g.$.DISMISSED,R(n),e(t)}},d.createElement("span",{className:y(S.u)},"Got it")))))}}),[U]);return!M||V||O?null:te?le||re||!ie||!ie.length||ae<5?null:d.createElement(P.cW,{source:{name:"blogrolls_sidebar",postId:K.postId||void 0,catalogId:K.catalogId||void 0}},d.createElement(E.x,{ref:Q,position:"relative",borderTop:m?"BASE_LIGHTER":"NONE",borderBottom:a?"NONE":void 0},d.createElement(E.x,{marginTop:"32px",marginBottom:"32px"},d.createElement(g.o,{flag:W,isVisible:r&&Y,targetDistance:15,renderFn:se},d.createElement("span",{className:y({textTransform:"uppercase",marginBottom:"8px"})},d.createElement(_.F,{scale:"S",tag:"span"},"".concat(l.name," Follows"))),d.createElement("ul",{className:y({marginTop:"8px"})},ie.map((function(e){return d.createElement("li",{className:y({display:"grid",gridTemplateColumns:"auto 1fr auto"}),key:null==e?void 0:e.id},d.createElement(E.x,{paddingRight:"12px"},d.createElement(p.G,{link:!0,publisher:e,scale:"XXXS"})),d.createElement("section",{className:y({wordBreak:"break-word"})},d.createElement($,{entity:e,tag:f})))}))),d.createElement(_.F,{scale:"S"},d.createElement(w.r,{linkStyle:"SUBTLE",href:T},"See all (".concat((0,L.rR)(ae),")"))))))):(ee(),null)},W=(0,u.Ps)(R()),Y=(0,u.Ps)(U(),b.b5,T.$),X=(0,u.Ps)(k(),p.v),q=(0,u.Ps)(j(),y.OJ,f.g,X)},44935:(e,n,t)=>{"use strict";t.d(n,{L:()=>p,g:()=>b});var l=t(28655),r=t.n(l),o=t(71439),i=t(67294),a=t(73882),s=t(84783),c=t(42933),u=t(37278),d=t(98024);function m(){var e=r()(["\n  fragment CollectionTooltip_collection on Collection {\n    id\n    name\n    description\n    subscriberCount\n    ...CollectionAvatar_collection\n    ...CollectionFollowButton_collection\n  }\n  ","\n  ","\n"]);return m=function(){return e},e}var p=function(e){var n=e.collection,t=e.buttonSize,l=e.buttonStyleFn,r=n.name,o=n.description;return i.createElement(c.x,{padding:"15px",display:"flex",flexDirection:"column",width:"300px"},i.createElement(c.x,{display:"flex",flexDirection:"row",justifyContent:"space-between",whiteSpace:"normal",borderBottom:"BASE_LIGHTER",paddingBottom:"10px",marginBottom:"10px"},i.createElement(c.x,{display:"flex",flexDirection:"column",paddingRight:"5px"},i.createElement(u.X6,{scale:"S"},r),i.createElement(d.F,{scale:"S"},o)),i.createElement(c.x,null,i.createElement(a.v,{collection:n,link:!0}))),i.createElement(c.x,{display:"flex",flexDirection:"row",alignItems:"center",justifyContent:"space-between"},i.createElement(d.F,{scale:"M"},"Followed by ",n.subscriberCount," people"),i.createElement(s.Fp,{collection:n,simpleButton:!0,buttonSize:t,buttonStyleFn:l,susiEntry:"follow_card"})))},b=(0,o.Ps)(m(),a.d,s.Iq)}}]);
//# sourceMappingURL=https://stats.medium.build/lite/sourcemaps/8886.309da8fb.chunk.js.map